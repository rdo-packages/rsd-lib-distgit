%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
%if 0%{?fedora} >= 24
%global with_python3 1
%endif

Name:           python-rsd-lib
Version:        XXX
Release:        XXX
Summary:        Python library for interfacing with Intel Rack Scale Design enabled hardware.

License:        ASL 2.0
URL:            https://github.com/openstack/%{name}
Source0:        http://tarballs.openstack.org/%{name}/%{name}-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  python-devel
BuildConflicts: python-coverage = 4.4
BuildRequires:  python-coverage >= 4.0
BuildRequires:  python-hacking >= 0.12.0
BuildRequires:  python-openstackdocstheme >= 1.11.0
BuildRequires:  python-oslotest >= 1.10.0
BuildRequires:  python-reno >= 1.8.0
BuildRequires:  python-setuptools
BuildRequires:  python-sphinx >= 1.6.2
BuildRequires:  python-subunit >= 0.0.18
BuildRequires:  python-testrepository >= 0.0.18
BuildRequires:  python-testtools >= 1.4.0
BuildRequires:  python-sphinx

Requires:       python-pbr >= 2.0
Requires:       python-sushy >= 0.1.0
Requires:       python-validictory >= 1.0.0

%description
This library extends the existing Sushy library to include functionality for
Intel RackScale Design enabled hardware. Capabilities include logical node
composition and decomposition, remote storage discovery and composition,
and NVMe over PCIe drive attaching and detaching to logical nodes.

%package -n     python2-rsd-lib
Summary:        %{summary}
%{?python_provide:%python_provide python2-rsd-lib}
Provides:       python-rsd-lib = %{upstream_version}

%if 0%{?with_python3}
%package -n     python3-rsd-lib
Summary:        %{summary}
%{?python_provide:%python_provide python3-rsd-lib}

BuildRequires:  python3-devel
BuildConflicts: python3-coverage = 4.4
BuildRequires:  python3-coverage >= 4.0
BuildRequires:  python3-hacking < 0.13
BuildRequires:  python3-hacking >= 0.12.0
BuildRequires:  python3-openstackdocstheme >= 1.11.0
BuildRequires:  python3-oslotest >= 1.10.0
BuildRequires:  python3-reno >= 1.8.0
BuildRequires:  python3-setuptools
BuildRequires:  python3-sphinx >= 1.6.2
BuildRequires:  python3-subunit >= 0.0.18
BuildRequires:  python3-testrepository >= 0.0.18
BuildRequires:  python3-testtools >= 1.4.0
BuildRequires:  python3-sphinx

Requires:       python3-pbr >= 2.0
Requires:       python3-sushy >= 0.1.0
Requires:       python3-validictory >= 1.0.0

%description
This library extends the existing Sushy library to include functionality for
Intel RackScale Design enabled hardware. Capabilities include logical node
composition and decomposition, remote storage discovery and composition,
and NVMe over PCIe drive attaching and detaching to logical nodes.

%endif # with_python3

%prep
%autosetup -n python-rsd-lib
# Remove bundled egg-info
rm -rf python-rsd-lib.egg-info

%build
%py2_build
%if 0%{?with_python3}
%py3_build
%endif

# generate html docs
sphinx-build-2 doc/source html
# remove the sphinx-build leftovers
rm -rf html/.{doctrees,buildinfo}

%install
%py2_install
%if 0%{?with_python3}
%py3_install
%endif

%check
%if 0%{?with_python3}
%{__python3} setup.py test
rm -rf .testrepository
%endif
%{__python2} setup.py test

%files -n python-rsd-lib
%license LICENSE
%doc doc/source/readme.rst README.rst
%{python2_sitelib}/rsd-lib
%{python2_sitelib}/rsd-lib-%{version}-py?.?.egg-info
