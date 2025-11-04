<template>
  <div class="item-detail">
    <div class="header">
      <h1>{{ isNewItem ? 'Create New Item' : 'Edit Item' }}</h1>
      <button @click="goBack" class="btn-secondary">Back to List</button>
    </div>

    <div v-if="loading" class="loading">Loading...</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    
    <form v-else @submit.prevent="saveItem" class="detail-form">
      <div class="form-group">
        <label for="name">Name *</label>
        <input
          id="name"
          v-model="item.name"
          @blur="autoSave"
          type="text"
          required
          class="form-control"
        />
      </div>

      <div class="form-group">
        <label for="description">Description</label>
        <textarea
          id="description"
          v-model="item.description"
          @blur="autoSave"
          rows="4"
          class="form-control"
        ></textarea>
      </div>

      <div class="form-row">
        <div class="form-group">
          <label for="category">Category</label>
          <input
            id="category"
            v-model="item.category"
            @blur="autoSave"
            type="text"
            class="form-control"
          />
        </div>

        <div class="form-group">
          <label for="quantity">Quantity *</label>
          <input
            id="quantity"
            v-model.number="item.quantity"
            @blur="autoSave"
            type="number"
            required
            class="form-control"
          />
        </div>
      </div>

      <div class="form-row">
        <div class="form-group">
          <label for="price">Price *</label>
          <input
            id="price"
            v-model.number="item.price"
            @blur="autoSave"
            type="number"
            step="0.01"
            required
            class="form-control"
          />
        </div>

        <div class="form-group">
          <label for="is_active">Active</label>
          <div class="form-control-checkbox">
            <input
              id="is_active"
              v-model="item.is_active"
              @change="autoSave"
              type="checkbox"
            />
          </div>
        </div>
      </div>

      <div class="save-status" v-if="saveStatus">
        {{ saveStatus }}
      </div>

      <div class="form-actions">
        <button type="submit" class="btn-primary">Save Manually</button>
        <button type="button" @click="goBack" class="btn-secondary">Cancel</button>
      </div>
    </form>
  </div>
</template>

<script>
import { itemApi } from '../services/api';

export default {
  name: 'ItemDetail',
  data() {
    return {
      item: {
        name: '',
        description: '',
        category: '',
        quantity: 0,
        price: 0.00,
        is_active: true,
      },
      originalItem: {},
      loading: false,
      error: null,
      saveStatus: '',
      saveTimeout: null,
      hasUnsavedChanges: false,
    };
  },
  computed: {
    isNewItem() {
      return this.$route.params.id === undefined || this.$route.name === 'ItemNew';
    },
  },
  mounted() {
    if (!this.isNewItem) {
      this.loadItem();
    }
    // Add beforeunload event listener to save before page close
    window.addEventListener('beforeunload', this.handleBeforeUnload);
    window.addEventListener('keydown', this.handleEscKey);
  },
  beforeUnmount() {
    // Clean up event listener
    window.removeEventListener('beforeunload', this.handleBeforeUnload);
    window.removeEventListener('keydown', this.handleEscKey);
    // Save any pending changes before component unmounts
    if (this.hasUnsavedChanges && !this.isNewItem) {
      this.saveItemSync();
    }
  },
  beforeRouteLeave(to, from, next) {
    // Auto-save before navigating away
    if (this.hasUnsavedChanges && !this.isNewItem) {
      this.saveItem().then(() => {
        next();
      }).catch(() => {
        next();
      });
    } else {
      next();
    }
  },
  methods: {
    async loadItem() {
      this.loading = true;
      this.error = null;
      try {
        const response = await itemApi.getOne(this.$route.params.id);
        this.item = { ...response.data };
        this.originalItem = { ...response.data };
        this.hasUnsavedChanges = false;
      } catch (err) {
        this.error = 'Failed to load item: ' + (err.message || 'Unknown error');
      } finally {
        this.loading = false;
      }
    },
    async saveItem() {
      this.error = null;
      this.saveStatus = 'Saving...';
      
      try {
        if (this.isNewItem) {
          const response = await itemApi.create(this.item);
          this.item = response.data;
          this.originalItem = { ...response.data };
          this.saveStatus = 'Saved successfully!';
          this.hasUnsavedChanges = false;
          // Redirect to edit mode after creation
          setTimeout(() => {
            this.$router.replace(`/items/${response.data.id}`);
          }, 500);
        } else {
          const response = await itemApi.update(this.$route.params.id, this.item);
          this.item = response.data;
          this.originalItem = { ...response.data };
          this.saveStatus = 'Saved successfully!';
          this.hasUnsavedChanges = false;
        }
        
        // Clear status message after 2 seconds
        setTimeout(() => {
          this.saveStatus = '';
        }, 2000);
      } catch (err) {
        this.error = 'Failed to save item: ' + (err.response?.data?.message || err.message || 'Unknown error');
        this.saveStatus = 'Save failed!';
        setTimeout(() => {
          this.saveStatus = '';
        }, 3000);
      }
    },
    autoSave() {
      // Check if there are actual changes
      const hasChanges = JSON.stringify(this.item) !== JSON.stringify(this.originalItem);
      
      if (hasChanges && !this.isNewItem) {
        this.hasUnsavedChanges = true;
        
        // Debounce: Clear previous timeout and set new one
        if (this.saveTimeout) {
          clearTimeout(this.saveTimeout);
        }
        
        // Save after 500ms of inactivity
        this.saveTimeout = setTimeout(() => {
          this.saveItem();
        }, 500);
      }
    },
    saveItemSync() {
      // Synchronous save for beforeunload (using sendBeacon if available)
      if (navigator.sendBeacon) {
        const data = new Blob([JSON.stringify(this.item)], { type: 'application/json' });
        navigator.sendBeacon(`http://localhost:8000/api/items/${this.$route.params.id}/`, data);
      }
    },
    handleBeforeUnload() {
      if (this.hasUnsavedChanges && !this.isNewItem) {
        // Save changes before unload
        this.saveItemSync();
      }
    },
    goBack() {
      this.$router.push('/items');
    },
    handleEscKey(event) {
      if (event.key === 'Escape') {
        this.goBack();
      }
    },
  },
};
</script>

<style scoped>
.item-detail {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.detail-form {
  background: white;
  padding: 30px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.form-group {
  margin-bottom: 20px;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
  color: #333;
}

.form-control {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
  box-sizing: border-box;
}

.form-control:focus {
  outline: none;
  border-color: #42b983;
}

textarea.form-control {
  resize: vertical;
}

.form-actions {
  display: flex;
  gap: 10px;
  margin-top: 30px;
}

.btn-primary {
  background-color: #42b983;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
}

.btn-primary:hover {
  background-color: #369870;
}

.btn-secondary {
  background-color: #6c757d;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
}

.btn-secondary:hover {
  background-color: #5a6268;
}

.save-status {
  margin-top: 10px;
  padding: 10px;
  border-radius: 4px;
  background-color: #d4edda;
  color: #155724;
  text-align: center;
}

.loading, .error {
  text-align: center;
  padding: 40px;
  font-size: 18px;
}

.error {
  color: #dc3545;
  background-color: #f8d7da;
  border: 1px solid #f5c6cb;
  border-radius: 4px;
  padding: 15px;
  margin-bottom: 20px;
}

/* Hide spin buttons for number inputs */
input[type="number"]::-webkit-outer-spin-button,
input[type="number"]::-webkit-inner-spin-button {
  -webkit-appearance: none;
  margin: 0;
}

input[type="number"] {
  -moz-appearance: textfield; /* Firefox */
}

.form-control-checkbox {
  display: flex;
  justify-content: flex-start;
  padding-top: 10px;
}

.form-control-checkbox input[type="checkbox"] {
  width: auto;
  margin-top: 0;
}
</style>
