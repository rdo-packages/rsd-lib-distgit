Name:           rsd-lib
Version:        XXX
Release:        XXX
Summary:        Python library for interfacing with Intel Rack Scale Design enabled hardware.

License:        ASL 2.0
URL:            https://github.com/openstack/%{name}
Source0:        http://tarballs.openstack.org/%{name}/%{name}-%{version}.tar.gz
BuildArch:      noarch
 
BuildRequires:  python2-devel
BuildConflicts: python2-coverage = 4.4
BuildRequires:  python2-coverage >= 4.0
BuildRequires:  python2-hacking < 0.13
BuildRequires:  python2-hacking >= 0.12.0
BuildRequires:  python2-openstackdocstheme >= 1.11.0
BuildRequires:  python2-oslotest >= 1.10.0
BuildRequires:  python2-reno >= 1.8.0
BuildRequires:  python2-setuptools
BuildRequires:  python2-sphinx >= 1.6.2
BuildRequires:  python2-subunit >= 0.0.18
BuildRequires:  python2-testrepository >= 0.0.18
BuildRequires:  python2-testtools >= 1.4.0
BuildRequires:  python2-sphinx

%description
This library extends the existing Sushy library to include functionality for
Intel RackScale Design enabled hardware. Capabilities include logical node
composition and decomposition, remote storage discovery and composition,
and NVMe over PCIe drive attaching and detaching to logical nodes.

%package -n     rsd-lib
Summary:        %{summary}
 
Requires:       python2-pbr >= 2.0
Requires:       python2-sushy >= 0.1.0
Requires:       python2-validictory >= 1.0.0

%prep
%autosetup -n rsd-lib
# Remove bundled egg-info
rm -rf rsd-lib.egg-info

%build
%py2_build
# generate html docs 
sphinx-build-2 doc/source html
# remove the sphinx-build leftovers
rm -rf html/.{doctrees,buildinfo}

%install
%py2_install

%check
%{__python2} setup.py test

%files -n rsd-lib
%license LICENSE
%doc doc/source/readme.rst README.rst
%{python2_sitelib}/rsd_lib
%{python2_sitelib}/rsd_lib-%{version}-py?.?.egg-info
