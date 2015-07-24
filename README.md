# Vagrant-sof-gluster

Type: `vagrant up` to start

### Troubleshooting

If you are using VirtualBox and happen to see the following error:

~~~
The provider 'libvirt' could not be found, but was requested to
back the machine 'client'. Please use a provider that exists.
~~~

Add `export VAGRANT_DEFAULT_PROVIDER=virtualbox` to your ~/.bashrc file
