%define vendor_name Intel
%define vendor_label intel
%define driver_name ixgbe

# XCP-ng: install to the override directory
%define module_dir override

Summary: %{vendor_name} %{driver_name} device drivers
Name: %{vendor_label}-%{driver_name}-alt
Version: 5.9.4
Release: 1%{?dist}
License: GPL

# Downloaded from https://downloadcenter.intel.com/download/14687/Intel-Network-Adapter-Driver-for-PCIe-Intel-10-Gigabit-Ethernet-Network-Connections-under-Linux-
Source0: ixgbe-%{version}.tar.gz

BuildRequires: gcc
BuildRequires: kernel-devel
Provides: vendor-driver
Requires: kernel-uname-r = %{kernel_version}
Requires(post): /usr/sbin/depmod
Requires(postun): /usr/sbin/depmod

%description
%{vendor_name} %{driver_name} device drivers for the Linux Kernel
version %{kernel_version}.

%prep
%autosetup -p1 -n ixgbe-%{version}

%build
%{?cov_wrap} %{make_build} -C /lib/modules/%{kernel_version}/build M=$(pwd)/src KSRC=/lib/modules/%{kernel_version}/build modules

%install
%{?cov_wrap} %{__make} %{?_smp_mflags} -C /lib/modules/%{kernel_version}/build M=$(pwd)/src INSTALL_MOD_PATH=%{buildroot} INSTALL_MOD_DIR=%{module_dir} DEPMOD=/bin/true modules_install

# mark modules executable so that strip-to-file can strip them
find %{buildroot}/lib/modules/%{kernel_version} -name "*.ko" -type f | xargs chmod u+x

%post
/sbin/depmod %{kernel_version}
%{regenerate_initrd_post}

%postun
/sbin/depmod %{kernel_version}
%{regenerate_initrd_postun}

%posttrans
%{regenerate_initrd_posttrans}

%files
/lib/modules/%{kernel_version}/*/*.ko

%changelog
* Fri Jan 08 2021 Samuel Verschelde <stormi-xcp@ylix.fr> - 5.9.4-1
- initial package, version 5.9.4
