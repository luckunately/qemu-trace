# Create a swap file of 64GB (65536 blocks of 1MB each) filled with zeros
sudo dd if=/dev/zero of=/swapfile bs=1M count=65536

# Set the correct permissions for the swap file to be readable and writable only by root
sudo chmod 600 /swapfile

# Set up the swap file
sudo mkswap /swapfile

# Enable the swap file for use
sudo swapon /swapfile

# Add the swap file entry to /etc/fstab to make the change permanent
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
