# -*- mode: ruby -*-
# vi: set ft=ruby :

VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|

  config.vm.box = "Trusty64"
  config.vm.box_url = "http://cloud-images.ubuntu.com/vagrant/trusty/trusty-server-cloudimg-amd64-juju-vagrant-disk1.box"

  config.vm.synced_folder ".", "/srv/pycnikr"

  config.vm.network :forwarded_port, host: 8001, guest: 8000
  config.vm.network :forwarded_port, host: 8081, guest: 8080

  config.vm.provision :shell, :privileged => false, :inline => "sh /srv/pycnikr/Vagrant/setup.sh"

end
