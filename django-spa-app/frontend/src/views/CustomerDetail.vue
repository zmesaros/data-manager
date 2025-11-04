<template>
  <div class="customer-detail">
    <div class="header">
      <h1>{{ isNewCustomer ? 'Create New Customer' : 'Edit Customer' }}</h1>
      <button @click="goBack" class="btn-secondary">Back to List</button>
    </div>

    <div v-if="loading" class="loading">Loading...</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    
    <form v-else @submit.prevent="saveCustomer" class="detail-form">
      <div class="form-row">
        <div class="form-group">
          <label for="first_name">First Name *</label>
          <input
            id="first_name"
            v-model="customer.first_name"
            @blur="autoSave"
            type="text"
            required
            class="form-control"
          />
        </div>

        <div class="form-group">
          <label for="last_name">Last Name *</label>
          <input
            id="last_name"
            v-model="customer.last_name"
            @blur="autoSave"
            type="text"
            required
            class="form-control"
          />
        </div>
      </div>

      <div class="form-row">
        <div class="form-group">
          <label for="email">Email *</label>
          <input
            id="email"
            v-model="customer.email"
            @blur="autoSave"
            type="email"
            required
            class="form-control"
          />
        </div>

        <div class="form-group">
          <label for="phone">Phone</label>
          <input
            id="phone"
            v-model="customer.phone"
            @blur="autoSave"
            type="text"
            class="form-control"
          />
        </div>
      </div>

      <div class="form-group">
        <label for="address">Address</label>
        <textarea
          id="address"
          v-model="customer.address"
          @blur="autoSave"
          rows="3"
          class="form-control"
        ></textarea>
      </div>

      <div class="form-row">
        <div class="form-group">
          <label for="city">City</label>
          <input
            id="city"
            v-model="customer.city"
            @blur="autoSave"
            type="text"
            class="form-control"
          />
        </div>

        <div class="form-group">
          <label for="country">Country</label>
          <input
            id="country"
            v-model="customer.country"
            @blur="autoSave"
            type="text"
            class="form-control"
          />
        </div>
      </div>

      <div class="form-group">
        <label for="is_active">
          <input
            id="is_active"
            v-model="customer.is_active"
            @change="autoSave"
            type="checkbox"
          />
          Active
        </label>
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
import { customerApi } from '../services/api';

export default {
  name: 'CustomerDetail',
  data() {
    return {
      customer: {
        first_name: '',
        last_name: '',
        email: '',
        phone: '',
        address: '',
        city: '',
        country: '',
        is_active: true,
      },
      originalCustomer: {},
      loading: false,
      error: null,
      saveStatus: '',
      saveTimeout: null,
      hasUnsavedChanges: false,
    };
  },
  computed: {
    isNewCustomer() {
      return this.$route.params.id === undefined || this.$route.name === 'CustomerNew';
    },
  },
  mounted() {
    if (!this.isNewCustomer) {
      this.loadCustomer();
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
    if (this.hasUnsavedChanges && !this.isNewCustomer) {
      this.saveCustomerSync();
    }
  },
  beforeRouteLeave(to, from, next) {
    // Auto-save before navigating away
    if (this.hasUnsavedChanges && !this.isNewCustomer) {
      this.saveCustomer().then(() => {
        next();
      }).catch(() => {
        next();
      });
    } else {
      next();
    }
  },
  methods: {
    async loadCustomer() {
      this.loading = true;
      this.error = null;
      try {
        const response = await customerApi.getOne(this.$route.params.id);
        this.customer = { ...response.data };
        this.originalCustomer = { ...response.data };
        this.hasUnsavedChanges = false;
      } catch (err) {
        this.error = 'Failed to load customer: ' + (err.message || 'Unknown error');
      } finally {
        this.loading = false;
      }
    },
    async saveCustomer() {
      this.error = null;
      this.saveStatus = 'Saving...';
      
      try {
        if (this.isNewCustomer) {
          const response = await customerApi.create(this.customer);
          this.customer = response.data;
          this.originalCustomer = { ...response.data };
          this.saveStatus = 'Saved successfully!';
          this.hasUnsavedChanges = false;
          // Redirect to edit mode after creation
          setTimeout(() => {
            this.$router.replace(`/customers/${response.data.id}`);
          }, 500);
        } else {
          const response = await customerApi.update(this.$route.params.id, this.customer);
          this.customer = response.data;
          this.originalCustomer = { ...response.data };
          this.saveStatus = 'Saved successfully!';
          this.hasUnsavedChanges = false;
        }
        
        // Clear status message after 2 seconds
        setTimeout(() => {
          this.saveStatus = '';
        }, 2000);
      } catch (err) {
        this.error = 'Failed to save customer: ' + (err.response?.data?.message || err.message || 'Unknown error');
        this.saveStatus = 'Save failed!';
        setTimeout(() => {
          this.saveStatus = '';
        }, 3000);
      }
    },
    autoSave() {
      // Check if there are actual changes
      const hasChanges = JSON.stringify(this.customer) !== JSON.stringify(this.originalCustomer);
      
      if (hasChanges && !this.isNewCustomer) {
        this.hasUnsavedChanges = true;
        
        // Debounce: Clear previous timeout and set new one
        if (this.saveTimeout) {
          clearTimeout(this.saveTimeout);
        }
        
        // Save after 500ms of inactivity
        this.saveTimeout = setTimeout(() => {
          this.saveCustomer();
        }, 500);
      }
    },
    saveCustomerSync() {
      // Synchronous save for beforeunload (using sendBeacon if available)
      if (navigator.sendBeacon) {
        const data = new Blob([JSON.stringify(this.customer)], { type: 'application/json' });
        navigator.sendBeacon(`http://localhost:8000/api/customers/${this.$route.params.id}/`, data);
      }
    },
    handleBeforeUnload() {
      if (this.hasUnsavedChanges && !this.isNewCustomer) {
        // Save changes before unload
        this.saveCustomerSync();
      }
    },
    goBack() {
      this.$router.push('/customers');
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
.customer-detail {
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
</style>
