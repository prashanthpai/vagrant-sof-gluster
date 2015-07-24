# -*- mode: ruby -*-
# vi: set ft=ruby :
#

# Things are hardcoded elsewhere, changing NODES and DISKS here wouldn't work
# unless you change it everywhere in other files
NODES = 4
DISKS = 4

# Disk size in MB
DISK_SIZE = 500*1024

# Possible values : "centos7" and "fedora22"
# fedora22 is broken as of now
BOX="centos7"

Vagrant.configure("2") do |config|

    if BOX == "centos7"
        config.vm.box = "chef/centos-7.1"
    end
    if BOX == "fedora22"
        config.vm.box = "boxcutter/fedora22"
    end

    config.ssh.insert_key = false

    # Make the glusterfs cluster, each with DISKS number of drives
    (1..NODES).each do |i|
        config.vm.define "storage#{i}" do |storage|
            storage.vm.hostname = "storage#{i}"
            storage.vm.network :private_network, ip: "192.168.10.10#{i}", netmask: "255.255.255.0"
            storage.vm.provider :virtualbox do |vb|
                vb.customize ["modifyvm", :id, "--natdnshostresolver1", "on"]
                if BOX == "fedora22"
                    # Some boxes does not have SATA controller, so we add one here
                    # Comment this out if you get an error that controller exists
                    # Refer: https://gist.github.com/leifg/4713995
                    #        https://github.com/mitchellh/vagrant/issues/4015
                    vb.customize(['storagectl', :id, '--name', 'SATA Controller', '--add', 'sata'])
                end
                vb.memory = 768
                vb.cpus = 2
                (1..DISKS).each do |d|
                    disk_file = "disks/disk-#{i}-#{d}.vdi"
                    unless File.exist?(disk_file)
                        vb.customize [ "createhd", "--filename", disk_file, "--size", DISK_SIZE ]
                    end
                    vb.customize [ "storageattach", :id, "--storagectl", "SATA Controller", "--port", 3+d, "--device", 0, "--type", "hdd", "--medium", "disks/disk-#{i}-#{d}.vdi" ]
                end
            end

            if i == (NODES)
                # View the documentation for the provider you're using for more
                # information on available options.
                storage.vm.provision :ansible do |ansible|
                    ansible.limit = "all"
                    ansible.playbook = "site.yml"
                    ansible.groups = {
                        "storage" => (1..NODES).map {|j| "storage#{j}"},
                    }
                end
            end
        end

    end
end
