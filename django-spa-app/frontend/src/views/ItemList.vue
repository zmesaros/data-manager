<template>
  <div class="item-list">
    <div class="header sticky-header">
      <h1>Items</h1>
      <input type="text" v-model="searchQuery" placeholder="Search..." class="search-input" />
    </div>

    <div v-if="loading" class="loading">Loading...</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    
    <div v-else class="table-container">
      <table class="data-table">
        <thead>
          <tr>
            <th @click="sortBy('id')">ID <span v-if="sortKey === 'id'" v-html="sortAsc ? '&#x25B2;' : '&#x25BC;'"></span></th>
            <th @click="sortBy('name')">Name <span v-if="sortKey === 'name'" v-html="sortAsc ? '&#x25B2;' : '&#x25BC;'"></span></th>
            <th @click="sortBy('category')">Category <span v-if="sortKey === 'category'" v-html="sortAsc ? '&#x25B2;' : '&#x25BC;'"></span></th>
            <th @click="sortBy('quantity')">Quantity <span v-if="sortKey === 'quantity'" v-html="sortAsc ? '&#x25B2;' : '&#x25BC;'"></span></th>
            <th @click="sortBy('price')">Price <span v-if="sortKey === 'price'" v-html="sortAsc ? '&#x25B2;' : '&#x25BC;'"></span></th>
            <th @click="sortBy('is_active')">Active <span v-if="sortKey === 'is_active'" v-html="sortAsc ? '&#x25B2;' : '&#x25BC;'"></span></th>
          </tr>
        </thead>
        <tbody @keydown="handleKeydown">
          <tr v-for="(item, rowIndex) in filteredAndSortedItems" :key="item.id" @click="selectItem(item)" :class="{ 'selected-row': item.id === selectedItemId }">
            <td @click.stop="viewDetail(item.id)" class="clickable-id">{{ item.id }}</td>
            <td>
              <input 
                type="text"
                v-model="item.name"
                @blur="saveItem(item); exitEditMode()"
                @focus="startEditMode(rowIndex, 0)"
                @keydown.f2="startEditMode(rowIndex, 0, $event)"
                @keydown.esc="exitEditMode(true)"
                @keydown.tab="saveItem(item); exitEditMode()"
                class="inline-edit-input"
                :data-row-index="rowIndex"
                data-col-index="0"
                :ref="`input-${rowIndex}-0`"
              />
            </td>
            <td>
              <input 
                type="text"
                v-model="item.category"
                @blur="saveItem(item); exitEditMode()"
                @focus="startEditMode(rowIndex, 1)"
                @keydown.f2="startEditMode(rowIndex, 1, $event)"
                @keydown.esc="exitEditMode(true)"
                @keydown.tab="saveItem(item); exitEditMode()"
                class="inline-edit-input"
                :data-row-index="rowIndex"
                data-col-index="1"
                :ref="`input-${rowIndex}-1`"
              />
            </td>
            <td>
              <input 
                :type="editingCell.rowIndex === rowIndex && editingCell.colIndex === 2 ? 'text' : 'number'"
                v-model.number="item.quantity"
                @blur="saveItem(item); exitEditMode()"
                @focus="startEditMode(rowIndex, 2)"
                @keydown.f2="startEditMode(rowIndex, 2, $event)"
                @keydown.esc="exitEditMode(true)"
                @keydown.tab="saveItem(item); exitEditMode()"
                class="inline-edit-input"
                :data-row-index="rowIndex"
                data-col-index="2"
                :ref="`input-${rowIndex}-2`"
              />
            </td>
            <td>
              <input 
                :type="editingCell.rowIndex === rowIndex && editingCell.colIndex === 3 ? 'text' : 'number'"
                v-model.number="item.price"
                @blur="saveItem(item); exitEditMode()"
                @focus="startEditMode(rowIndex, 3)"
                @keydown.f2="startEditMode(rowIndex, 3, $event)"
                @keydown.esc="exitEditMode(true)"
                @keydown.tab="saveItem(item); exitEditMode()"
                class="inline-edit-input"
                step="0.01"
                :data-row-index="rowIndex"
                data-col-index="3"
                :ref="`input-${rowIndex}-3`"
              />
            </td>
            <td>
              <input 
                type="checkbox"
                v-model="item.is_active"
                @change="saveItem(item)"
                @blur="saveItem(item); exitEditMode()"
                @focus="startEditMode(rowIndex, 4)"
                @keydown.esc="exitEditMode(true)"
                @keydown.tab="saveItem(item); exitEditMode()"
                :data-row-index="rowIndex"
                data-col-index="4"
                :ref="`input-${rowIndex}-4`"
              />
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="fab-container">
      <div class="fab-menu" :class="{ open: isMenuOpen }">
        <button @click="deleteSelectedItem" :disabled="!selectedItemId" class="fab-item btn-danger" title="Delete Selected">&#x1F5D1;</button>
        <button @click="addNewItem" class="fab-item btn-primary" title="New Item">&#x270E;</button>
      </div>
      <button @click="toggleMenu" class="fab-main"><span>+</span></button>
    </div>
  </div>
</template>

<script>
import { itemApi } from '../services/api';
import axios from 'axios';

export default {
  name: 'ItemList',
  data() {
    return {
      items: [],
      loading: false,
      error: null,
      saveTimeout: null,
      emptyItemAdded: false,
      isCreatingNewItem: false,
      selectedItemId: null,
      isMenuOpen: false,
      sortKey: '',
      sortAsc: true,
      searchQuery: '',
      editingCell: { rowIndex: null, colIndex: null },
      isEditingActive: false,
      sortedItemsSnapshot: [],
    };
  },
  computed: {
    filteredItems() {
      if (!this.searchQuery) {
        return this.items;
      }
      const lowerCaseQuery = this.searchQuery.toLowerCase();
      return this.items.filter(item => {
        return item.id === null || 
               (item.name && item.name.toLowerCase().includes(lowerCaseQuery)) ||
               (item.category && item.category.toLowerCase().includes(lowerCaseQuery));
      });
    },
    sortedItems() {
      if (!this.sortKey) {
        return this.filteredItems;
      }
      const sorted = [...this.filteredItems].sort((a, b) => {
        if (a.id === null) return 1;
        if (b.id === null) return -1;
        let valA = a[this.sortKey];
        let valB = b[this.sortKey];
        if (valA === null || valA === undefined) return 1;
        if (valB === null || valB === undefined) return -1;

        // Handle numeric sorting for 'price' and 'quantity'
        if (this.sortKey === 'price' || this.sortKey === 'quantity') {
          valA = parseFloat(valA);
          valB = parseFloat(valB);
        } else if (typeof valA === 'string') {
          valA = valA.toLowerCase();
          valB = valB.toLowerCase();
        }
        if (valA < valB) return this.sortAsc ? -1 : 1;
        if (valA > valB) return this.sortAsc ? 1 : -1;
        return 0;
      });
      return sorted;
    },
    filteredAndSortedItems() {
      if (this.isEditingActive) {
        return this.sortedItemsSnapshot;
      }
      return this.sortedItems;
    }
  },
  watch: {
    sortedItems: {
      handler(newVal) {
        if (!this.isEditingActive) {
          this.sortedItemsSnapshot = newVal;
        }
      },
      immediate: true
    },
    isEditingActive(newVal) {
      if (newVal === false) {
        this.$nextTick(() => {
          this.sortedItemsSnapshot = [...this.sortedItems];
        });
      }
    }
  },
  mounted() {
    this.loadAllItems();
  },
  beforeUnmount() {
    if (this.saveTimeout) clearTimeout(this.saveTimeout);
    this.handleItemDeselection(this.selectedItemId);
  },
  methods: {
    sortBy(key) {
      if (this.sortKey === key) this.sortAsc = !this.sortAsc;
      else { this.sortKey = key; this.sortAsc = true; }
    },
    toggleMenu() {
      this.isMenuOpen = !this.isMenuOpen;
    },
    selectItem(item) {
      if (this.selectedItemId === item.id) return;
      this.handleItemDeselection(this.selectedItemId);
      if (item) this.selectedItemId = item.id;
      else this.selectedItemId = null;
    },
    handleItemDeselection(previousItemId) {
      const previousItem = this.items.find(i => i.id === previousItemId);
      if (previousItem && previousItem.id === null) {
        const isEmpty = !(previousItem.name || previousItem.category || previousItem.quantity !== 0 || previousItem.price !== 0.00);
        if (isEmpty) {
          this.items = this.items.filter(i => i.id !== null);
          this.emptyItemAdded = false;
        } else {
          this.createItem(previousItem);
        }
      }
    },
    handleKeydown(event) {
      const { key } = event;
      const target = event.target;
      const isInput = target.tagName === 'INPUT';
      const currentRowIndex = parseInt(target.dataset.rowIndex, 10);
      const currentColIndex = parseInt(target.dataset.colIndex, 10);

      let preventDefault = false;

      if (isInput) {
        const isTextType = target.type === 'text';
        const cursorAtStart = target.selectionStart === 0;
        const cursorAtEnd = target.selectionEnd === target.value.length;

        if (key === 'ArrowLeft') {
          if (isTextType && !cursorAtStart) {
            return; // Allow cursor to move within the text input
          } else {
            preventDefault = true;
          }
        } else if (key === 'ArrowRight') {
          if (isTextType && !cursorAtEnd) {
            return; // Allow cursor to move within the text input
          } else {
            preventDefault = true;
          }
        } else if (['ArrowUp', 'ArrowDown'].includes(key)) {
          preventDefault = true;
        }
      }

      if (preventDefault) {
        event.preventDefault();
      }

      let nextRowIndex = currentRowIndex;
      let nextColIndex = currentColIndex;

      switch (key) {
        case 'ArrowUp':
          nextRowIndex = currentRowIndex > 0 ? currentRowIndex - 1 : -1; // -1 indicates no move
          break;
        case 'ArrowDown':
          nextRowIndex = currentRowIndex < this.filteredAndSortedItems.length - 1 ? currentRowIndex + 1 : -1;
          break;
        case 'ArrowLeft':
          nextColIndex = currentColIndex > 0 ? currentColIndex - 1 : -1;
          break;
        case 'ArrowRight':
          nextColIndex = currentColIndex < 4 ? currentColIndex + 1 : -1; // 4 is the last column index
          break;
        default:
          return;
      }

      if (nextRowIndex !== -1 && nextColIndex !== -1) {
        this.$nextTick(() => {
          const nextElement = this.$el.querySelector(`[data-row-index="${nextRowIndex}"][data-col-index="${nextColIndex}"]`);
          if (nextElement) {
            nextElement.focus();
            // If moving to a text input, set cursor to beginning/end based on arrow key
            if (nextElement.type === 'text') {
              if (key === 'ArrowLeft') {
                nextElement.setSelectionRange(nextElement.value.length, nextElement.value.length);
              } else if (key === 'ArrowRight') {
                nextElement.setSelectionRange(0, 0);
              }
            }
          }
        });
      }
    },
    async loadAllItems() {
      this.loading = true; this.error = null; this.selectedItemId = null;
      let allItems = [];
      try {
        let response = await itemApi.getAll();
        allItems = response.data.results;
        let next = response.data.next;
        while (next) {
          response = await axios.get(next);
          allItems = allItems.concat(response.data.results);
          next = response.data.next;
        }
        this.items = allItems;
      } catch (err) {
        this.error = 'Failed to load items: ' + (err.message || 'Unknown error');
      } finally { this.loading = false; }
    },
    viewDetail(id) { if (id) this.$router.push(`/items/${id}`); },
    addNewItem() {
      if (this.emptyItemAdded) return;
      this.handleItemDeselection(this.selectedItemId);
      const newItem = { id: null, name: '', category: '', quantity: 0, price: 0.00, is_active: true };
      this.items.push(newItem);
      this.emptyItemAdded = true;
      this.selectItem(newItem);
      this.isMenuOpen = false;
      this.$nextTick(() => {
        const newRow = this.$el.querySelector(`[data-row-index="${this.filteredAndSortedItems.length - 1}"] input`);
        if (newRow) newRow.focus();
      });
    },
    async deleteSelectedItem() {
      if (!this.selectedItemId) return;
      if (!confirm('Are you sure you want to delete this item?')) return;
      try {
        await itemApi.delete(this.selectedItemId);
        this.isMenuOpen = false;
        await this.loadAllItems();
      } catch (err) { alert('Failed to delete item: ' + (err.message || 'Unknown error')); }
    },
    saveItem(item) {
      if (!item.id) return; // Only save existing items on blur
      if (this.saveTimeout) clearTimeout(this.saveTimeout);
      this.saveTimeout = setTimeout(async () => {
        try {
          // Ensure item.price is a number and format to two decimal places before sending to backend
          if (item.price !== undefined && item.price !== null) {
            let priceValue = parseFloat(item.price);
            if (isNaN(priceValue)) {
              priceValue = 0;
            }
            item.price = parseFloat(priceValue.toFixed(2));
          }
          const response = await itemApi.update(item.id, item);
          // Update the local item with the response from the backend
          Object.assign(item, response.data);
          console.log(`Item ${item.id} updated successfully.`);
        } catch (err) {
          console.error(`Failed to save item ${item.id}:`, err);
          alert('Failed to save item: ' + (err.message || 'Unknown error'));
        }
      }, 500);
    },
    async createItem(item) {
      if (this.isCreatingNewItem) return;
      // For items, any field is enough to trigger a save, no alert needed.
      if (!item.name.trim() && !item.category.trim() && item.quantity === 0 && item.price === 0) {
          this.items = this.items.filter(i => i.id !== null); // Silently remove
          this.emptyItemAdded = false;
          return;
      }
      this.isCreatingNewItem = true;
      try {
        const newItemData = await itemApi.create(item);
        const index = this.items.findIndex(i => i.id === null);
        if (index !== -1) {
          Object.assign(this.items[index], newItemData.data);
          this.selectedItemId = newItemData.data.id;
        }
        this.emptyItemAdded = false;
      } catch (err) {
        console.error(`Failed to create item:`, err);
        alert('Failed to create item: ' + (err.message || 'Unknown error'));
      } finally {
        this.isCreatingNewItem = false;
      }
    },
    startEditMode(rowIndex, colIndex, event) {
      this.editingCell = { rowIndex, colIndex };
      this.isEditingActive = true; // Set editing flag
      if (event && event.key === 'F2') {
        event.preventDefault();
        this.$nextTick(() => {
          const inputRef = `input-${rowIndex}-${colIndex}`;
          const inputElement = this.$refs[inputRef];
          let elementToFocus = null;
          if (Array.isArray(inputElement)) {
            elementToFocus = inputElement[0];
          } else {
            elementToFocus = inputElement;
          }

          if (elementToFocus) {
            elementToFocus.focus();
            if (elementToFocus.type === 'text') {
              elementToFocus.setSelectionRange(elementToFocus.value.length, elementToFocus.value.length);
            }
          }
        });
      }
    },
    exitEditMode() {
      // For now, just exit edit mode. Revert logic can be added if needed.
      this.editingCell = { rowIndex: null, colIndex: null };
      this.isEditingActive = false; // Clear editing flag
    },
  },
};
</script>

<style scoped>
.item-list { max-width: 1200px; margin: 0 auto; padding: 20px; }
.header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }
.sticky-header { position: sticky; top: 0; background-color: white; z-index: 10; padding-top: 20px; padding-bottom: 20px; }
.search-input { padding: 8px 12px; border: 1px solid #ccc; border-radius: 4px; width: 300px; font-size: 14px; }
.table-container { margin-top: 20px; }
.data-table { width: 100%; border-collapse: collapse; background: white; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
.data-table th, .data-table td { padding: 2px 8px; text-align: left; }
.data-table th { background-color: #42b983; color: white; font-weight: bold; cursor: pointer; }
.clickable-id { cursor: pointer; font-weight: bold; color: #007bff; }
.clickable-id:hover { text-decoration: underline; }
.inline-edit-input { width: 100%; padding: 5px; border: 1px solid #ccc; border-radius: 4px; box-sizing: border-box; }
.selected-row { background-color: #e9f5ff; }
.fab-container { position: fixed; bottom: 30px; right: 30px; z-index: 1000; }
.fab-main { width: 60px; height: 60px; border-radius: 50%; background-color: #42b983; color: white; border: none; font-size: 28px; line-height: 60px; text-align: center; box-shadow: 0 4px 8px rgba(0,0,0,0.2); cursor: pointer; transition: transform 0.2s ease-in-out; }
.fab-main span { display: inline-block; transition: transform 0.2s ease-in-out; }
.fab-menu.open + .fab-main span { transform: rotate(45deg); }
.fab-menu { position: absolute; bottom: 70px; right: 5px; display: flex; flex-direction: column; gap: 15px; align-items: center; }
.fab-item { width: 48px; height: 48px; border-radius: 50%; color: white; border: none; font-size: 22px; line-height: 48px; text-align: center; box-shadow: 0 2px 6px rgba(0,0,0,0.2); cursor: pointer; transform: scale(0); transition: transform 0.2s ease-in-out, background-color 0.2s; }
.fab-menu.open .fab-item { transform: scale(1); }
.fab-item.btn-primary { background-color: #007bff; transition-delay: 0.1s; }
.fab-item.btn-primary:hover { background-color: #0056b3; }
.fab-item.btn-danger { background-color: #dc3545; transition-delay: 0.05s; }
.fab-item.btn-danger:hover { background-color: #c82333; }
.fab-item:disabled { background-color: #ccc; cursor: not-allowed; }
.loading, .error { text-align: center; padding: 40px; font-size: 18px; }
.error { color: #dc3545; }

/* Hide spin buttons for number inputs */
input[type="number"]::-webkit-outer-spin-button,
input[type="number"]::-webkit-inner-spin-button {
  -webkit-appearance: none;
  margin: 0;
}

input[type="number"] {
  -moz-appearance: textfield; /* Firefox */
}
</style>