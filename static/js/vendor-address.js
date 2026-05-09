/**
 * Vendor Address Selection Module
 * Handles dynamic loading of vendor addresses when vendor is selected
 */

// Load vendor addresses via AJAX when vendor is selected
function loadVendorAddresses(vendorId, selectedAddressId = null) {
    const addressSelect = document.getElementById('vendor_address_id');
    if (!addressSelect) {
        console.log('vendor_address_id element not found');
        return;
    }
    
    // Clear existing options
    addressSelect.innerHTML = '<option value="">-- Select Address --</option>';
    
    if (!vendorId) {
        addressSelect.disabled = true;
        return;
    }
    
    console.log('Loading addresses for vendor:', vendorId);
    
    // Fetch addresses from API
    fetch(`/api/vendors/${vendorId}/addresses`)
        .then(response => {
            console.log('Response status:', response.status);
            if (!response.ok) {
                throw new Error('Network response was not ok: ' + response.status);
            }
            return response.json();
        })
        .then(addresses => {
            console.log('Addresses loaded:', addresses);
            if (addresses && addresses.length > 0) {
                addresses.forEach(addr => {
                    const option = document.createElement('option');
                    option.value = addr.id;
                    const primaryLabel = addr.is_primary ? ' [PRIMARY]' : '';
                    option.textContent = `${addr.address_type}${primaryLabel}: ${addr.full_address}`;
                    if (selectedAddressId && addr.id === parseInt(selectedAddressId)) {
                        option.selected = true;
                    }
                    addressSelect.appendChild(option);
                });
                addressSelect.disabled = false;
                console.log('Address dropdown populated with', addresses.length, 'addresses');
            } else {
                addressSelect.innerHTML = '<option value="">No addresses found</option>';
                addressSelect.disabled = true;
                console.log('No addresses found for vendor');
            }
        })
        .catch(error => {
            console.error('Error loading vendor addresses:', error);
            addressSelect.innerHTML = '<option value="">Error loading addresses</option>';
            addressSelect.disabled = true;
        });
}

// Initialize vendor address dropdown on page load
function initVendorAddressModule() {
    const vendorSelect = document.getElementById('vendor_id');
    const addressSelect = document.getElementById('vendor_address_id');
    
    console.log('Initializing vendor address module');
    console.log('vendorSelect:', vendorSelect);
    console.log('addressSelect:', addressSelect);
    
    if (vendorSelect && addressSelect) {
        // Store the initially selected address (for edit mode)
        const selectedAddressId = addressSelect.dataset.selectedId || null;
        console.log('selectedAddressId:', selectedAddressId);
        
        // Load addresses for initial vendor selection
        if (vendorSelect.value) {
            console.log('Loading initial addresses for vendor:', vendorSelect.value);
            loadVendorAddresses(vendorSelect.value, selectedAddressId);
        } else {
            addressSelect.disabled = true;
        }
        
        // Handle vendor selection change
        vendorSelect.addEventListener('change', function() {
            console.log('Vendor changed to:', this.value);
            loadVendorAddresses(this.value);
        });
    } else {
        console.log('Vendor select or address select not found');
        console.log('Looking for vendor_id:', !!document.getElementById('vendor_id'));
        console.log('Looking for vendor_address_id:', !!document.getElementById('vendor_address_id'));
    }
}

// Try to initialize on DOMContentLoaded
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initVendorAddressModule);
} else {
    // DOM is already ready
    initVendorAddressModule();
}

// Export for use in other modules
window.VendorAddressModule = {
    loadVendorAddresses: loadVendorAddresses,
    init: initVendorAddressModule
};
