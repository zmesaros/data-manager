<template>
  <div class="customer-list">
    <div class="header sticky-header">
      <h1>Customers</h1>
      <input type="text" v-model="searchQuery" placeholder="Search..." class="search-input" />
    </div>

    <div v-if="loading" class="loading">Loading...</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    
    <div v-else class="table-container">
      <table class="data-table">
        <thead>
          <tr>
            <th @click="sortBy('id')">ID <span v-if="sortKey === 'id'" v-html="sortAsc ? '&#x25B2;' : '&#x25BC;'"></span></th>
            <th @click="sortBy('first_name')">First Name <span v-if="sortKey === 'first_name'" v-html="sortAsc ? '&#x25B2;' : '&#x25BC;'"></span></th>
            <th @click="sortBy('last_name')">Last Name <span v-if="sortKey === 'last_name'" v-html="sortAsc ? '&#x25B2;' : '&#x25BC;'"></span></th>
            <th @click="sortBy('email')">Email <span v-if="sortKey === 'email'" v-html="sortAsc ? '&#x25B2;' : '&#x25BC;'"></span></th>
            <th @click="sortBy('phone')">Phone <span v-if="sortKey === 'phone'" v-html="sortAsc ? '&#x25B2;' : '&#x25BC;'"></span></th>
            <th @click="sortBy('city')">City <span v-if="sortKey === 'city'" v-html="sortAsc ? '&#x25B2;' : '&#x25BC;'"></span></th>
            <th @click="sortBy('is_active')">Active <span v-if="sortKey === 'is_active'" v-html="sortAsc ? '&#x25B2;' : '&#x25BC;'"></span></th>
          </tr>
        </thead>
        <tbody @keydown="handleKeydown">
          <tr v-for="(customer, rowIndex) in filteredAndSortedCustomers" :key="customer.id" @click="selectCustomer(customer)" :class="{ 'selected-row': customer.id === selectedCustomerId }">
            <td @click.stop="viewDetail(customer.id)" class="clickable-id">{{ customer.id }}</td>
            <td>
              <input 
                type="text"
                v-model="customer.first_name"
                @blur="saveCustomer(customer); exitEditMode()"
                @focus="startEditMode(rowIndex, 0)"
                @keydown.f2="startEditMode(rowIndex, 0, $event)"
                @keydown.esc="exitEditMode()"
                @keydown.tab="saveCustomer(customer); exitEditMode()"
                class="inline-edit-input"
                :data-row-index="rowIndex"
                data-col-index="0"
                :ref="`input-${rowIndex}-0`"
              />
            </td>
            <td>
              <input 
                type="text"
                v-model="customer.last_name"
                @blur="saveCustomer(customer); exitEditMode()"
                @focus="startEditMode(rowIndex, 1)"
                @keydown.f2="startEditMode(rowIndex, 1, $event)"
                @keydown.esc="exitEditMode()"
                @keydown.tab="saveCustomer(customer); exitEditMode()"
                class="inline-edit-input"
                :data-row-index="rowIndex"
                data-col-index="1"
                :ref="`input-${rowIndex}-1`"
              />
            </td>
            <td>
              <input 
                type="email"
                v-model="customer.email"
                @blur="saveCustomer(customer); exitEditMode()"
                @focus="startEditMode(rowIndex, 2)"
                @keydown.f2="startEditMode(rowIndex, 2, $event)"
                @keydown.esc="exitEditMode()"
                @keydown.tab="saveCustomer(customer); exitEditMode()"
                class="inline-edit-input"
                :data-row-index="rowIndex"
                data-col-index="2"
                :ref="`input-${rowIndex}-2`"
              />
            </td>
            <td>
              <input 
                type="text"
                v-model="customer.phone"
                @blur="saveCustomer(customer); exitEditMode()"
                @focus="startEditMode(rowIndex, 3)"
                @keydown.f2="startEditMode(rowIndex, 3, $event)"
                @keydown.esc="exitEditMode()"
                @keydown.tab="saveCustomer(customer); exitEditMode()"
                class="inline-edit-input"
                :data-row-index="rowIndex"
                data-col-index="3"
                :ref="`input-${rowIndex}-3`"
              />
            </td>
            <td>
              <input 
                type="text"
                v-model="customer.city"
                @blur="saveCustomer(customer); exitEditMode()"
                @focus="startEditMode(rowIndex, 4)"
                @keydown.f2="startEditMode(rowIndex, 4, $event)"
                @keydown.esc="exitEditMode()"
                @keydown.tab="saveCustomer(customer); exitEditMode()"
                class="inline-edit-input"
                :data-row-index="rowIndex"
                data-col-index="4"
                :ref="`input-${rowIndex}-4`"
              />
            </td>
            <td>
              <input 
                type="checkbox"
                v-model="customer.is_active"
                @change="saveCustomer(customer)"
                @blur="saveCustomer(customer); exitEditMode()"
                @focus="startEditMode(rowIndex, 5)"
                @keydown.esc="exitEditMode()"
                @keydown.tab="saveCustomer(customer); exitEditMode()"
                :data-row-index="rowIndex"
                data-col-index="5"
                :ref="`input-${rowIndex}-5`"
              />
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="fab-container">
      <div class="fab-menu" :class="{ open: isMenuOpen }">
        <button @click="deleteSelectedCustomer" :disabled="!selectedCustomerId" class="fab-item btn-danger" title="Delete Selected">&#x1F5D1;</button>
        <button @click="addNewCustomer" class="fab-item btn-primary" title="New Customer">&#x270E;</button>
      </div>
      <button @click="toggleMenu" class="fab-main"><span>+</span></button>
    </div>
  </div>
</template>

<script>
import { customerApi } from '../services/api';
import axios from 'axios';

export default {
  name: 'CustomerList',
  data() {
    return {
      customers: [],
      loading: false,
      error: null,
      saveTimeout: null,
      emptyCustomerAdded: false,
      isCreatingNewItem: false,
      selectedCustomerId: null,
      isMenuOpen: false,
      sortKey: '',
      sortAsc: true,
      searchQuery: '',
      editingCell: { rowIndex: null, colIndex: null },
      isEditingActive: false,
      sortedCustomersSnapshot: [],
    };
  },
  computed: {
    filteredAndSortedCustomers() {
      let filtered = this.customers;
      if (this.searchQuery) {
        const lowerCaseQuery = this.searchQuery.toLowerCase();
        filtered = this.customers.filter(customer => {
          return customer.id === null || 
                 (customer.first_name && customer.first_name.toLowerCase().includes(lowerCaseQuery)) ||
                 (customer.last_name && customer.last_name.toLowerCase().includes(lowerCaseQuery)) ||
                 (customer.email && customer.email.toLowerCase().includes(lowerCaseQuery)) ||
                 (customer.phone && customer.phone.toLowerCase().includes(lowerCaseQuery)) ||
                 (customer.city && customer.city.toLowerCase().includes(lowerCaseQuery));
        });
      }
      if (!this.sortKey) {
        this.sortedCustomersSnapshot = filtered; // Update snapshot when not sorted
        return filtered;
      }

      // If a customer is being edited, return the snapshot to prevent focus loss
      if (this.isEditingActive) {
        return this.sortedCustomersSnapshot;
      }

      const sorted = [...filtered].sort((a, b) => {
        if (a.id === null) return 1;
        if (b.id === null) return -1;
        let valA = a[this.sortKey];
        let valB = b[this.sortKey];
        if (valA === null || valA === undefined) return 1;
        if (valB === null || valB === undefined) return -1;
        if (typeof valA === 'string') {
          valA = valA.toLowerCase();
          valB = valB.toLowerCase();
        }
        if (valA < valB) return this.sortAsc ? -1 : 1;
        if (valA > valB) return this.sortAsc ? 1 : -1;
        return 0;
      });
      this.sortedCustomersSnapshot = sorted; // Update snapshot after sorting
      return sorted;
    }
  },
  mounted() {
    this.loadAllCustomers();
  },
  beforeUnmount() {
    if (this.saveTimeout) clearTimeout(this.saveTimeout);
    this.handleItemDeselection(this.selectedCustomerId);
  },
  methods: {
    sortBy(key) {
      if (this.sortKey === key) this.sortAsc = !this.sortAsc;
      else { this.sortKey = key; this.sortAsc = true; }
    },
    toggleMenu() {
      this.isMenuOpen = !this.isMenuOpen;
    },
    selectCustomer(customer) {
      if (this.selectedCustomerId === customer.id) return;
      this.handleItemDeselection(this.selectedCustomerId);
      if (customer) this.selectedCustomerId = customer.id;
      else this.selectedCustomerId = null;
    },
    handleItemDeselection(previousCustomerId) {
      const previousCustomer = this.customers.find(c => c.id === previousCustomerId);
      if (previousCustomer && previousCustomer.id === null) {
        const isEmpty = !(previousCustomer.first_name.trim() || previousCustomer.last_name.trim() || previousCustomer.email.trim());
        if (isEmpty) {
          this.customers = this.customers.filter(c => c.id !== null);
          this.emptyCustomerAdded = false;
        } else {
          this.createCustomer(previousCustomer);
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
        const isTextType = target.type === 'text' || target.type === 'email';
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
          nextRowIndex = currentRowIndex < this.filteredAndSortedCustomers.length - 1 ? currentRowIndex + 1 : -1;
          break;
        case 'ArrowLeft':
          nextColIndex = currentColIndex > 0 ? currentColIndex - 1 : -1;
          break;
        case 'ArrowRight':
          nextColIndex = currentColIndex < 5 ? currentColIndex + 1 : -1; // 5 is the last column index
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
            if (nextElement.type === 'text' || nextElement.type === 'email') {
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
    async loadAllCustomers() {
      this.loading = true; this.error = null; this.selectedCustomerId = null;
      let allCustomers = [];
      try {
        let response = await customerApi.getAll();
        allCustomers = response.data.results;
        let next = response.data.next;
        while (next) {
          response = await axios.get(next);
          allCustomers = allCustomers.concat(response.data.results);
          next = response.data.next;
        }
        this.customers = allCustomers;
      } catch (err) {
        this.error = 'Failed to load customers: ' + (err.message || 'Unknown error');
      } finally { this.loading = false; }
    },
    viewDetail(id) { if (id) this.$router.push(`/customers/${id}`); },
    addNewCustomer() {
      if (this.emptyCustomerAdded) return;
      this.handleItemDeselection(this.selectedCustomerId);
      const newCustomer = { id: null, first_name: '', last_name: '', email: '', phone: '', city: '', is_active: true };
      this.customers.push(newCustomer);
      this.emptyCustomerAdded = true;
      this.selectCustomer(newCustomer);
      this.isMenuOpen = false;
      this.$nextTick(() => {
        const newRow = this.$el.querySelector(`[data-row-index="${this.filteredAndSortedCustomers.length - 1}"] input`);
        if (newRow) newRow.focus();
      });
    },
    async deleteSelectedCustomer() {
      if (!this.selectedCustomerId) return;
      if (!confirm('Are you sure you want to delete this customer?')) return;
      try {
        await customerApi.delete(this.selectedCustomerId);
        this.isMenuOpen = false;
        await this.loadAllCustomers();
      } catch (err) { alert('Failed to delete customer: ' + (err.message || 'Unknown error')); }
    },
    saveCustomer(customer) {
      if (!customer.id) return; // Only save existing customers on blur
      if (this.saveTimeout) clearTimeout(this.saveTimeout);
      this.saveTimeout = setTimeout(async () => {
        try {
          const response = await customerApi.update(customer.id, customer);
          // Update the local customer with the response from the backend
          Object.assign(customer, response.data);
          console.log(`Customer ${customer.id} updated successfully.`);
        } catch (err) {
          console.error(`Failed to save customer ${customer.id}:`, err);
          alert('Failed to save customer: ' + (err.message || 'Unknown error'));
        }
      }, 500);
    },
    async createCustomer(customer) {
      if (this.isCreatingNewItem) return;
      if (!customer.first_name.trim() || !customer.last_name.trim() || !customer.email.trim()) {
        alert('To save a new customer, First Name, Last Name, and Email are required.');
        return;
      }
      this.isCreatingNewItem = true;
      try {
        const newCustomerData = await customerApi.create(customer);
        const index = this.customers.findIndex(c => c.id === null);
        if (index !== -1) {
          Object.assign(this.customers[index], newCustomerData.data);
          this.selectedCustomerId = newCustomerData.data.id;
        }
        this.emptyCustomerAdded = false;
      } catch (err) {
        console.error(`Failed to create customer:`, err);
        alert('Failed to create customer: ' + (err.message || 'Unknown error'));
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
            if (elementToFocus.type === 'text' || elementToFocus.type === 'email') {
              elementToFocus.setSelectionRange(elementToFocus.value.length, elementToFocus.value.length);
            }
          }
        });
      }
    },
    exitEditMode() {
      this.editingCell = { rowIndex: null, colIndex: null };
      this.isEditingActive = false; // Clear editing flag
    },
  },
};
</script>

<style scoped>
.customer-list { max-width: 1200px; margin: 0 auto; padding: 20px; }
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
</style>
