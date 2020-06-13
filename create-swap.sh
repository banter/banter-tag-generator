sudo dd if=/dev/zero of=/root/myswapfile bs=1M count=1024
sudo mkswap /root/myswapfile
sudo chmod 600 /root/myswapfile
sudo swapon /root/myswapfile
sudo swapon -s