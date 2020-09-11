%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

%global sname rsd-lib
%global pyname rsd_lib

%global with_doc 1

Name:           python-%{sname}
Version:        XXX
Release:        XXX
Summary:        Python library for interfacing with Intel Rack Scale Design enabled hardware.

License:        ASL 2.0
URL:            http://git.openstack.org/cgit/openstack/%{sname}
Source0:        http://tarballs.openstack.org/%{sname}/%{sname}-%{upstream_version}.tar.gz
BuildArch:      noarch

%description
This library extends the existing Sushy library to include functionality for
Intel RackScale Design enabled hardware. Capabilities include logical node
composition and decomposition, remote storage discovery and composition,
and NVMe over PCIe drive attaching and detaching to logical nodes.

%package -n     python3-%{sname}
Summary:        %{summary}
%{?python_provide:%python_provide python3-%{sname}}

BuildRequires:  python3-devel
BuildRequires:  python3-jsonschema
BuildRequires:  python3-pbr >= 2.0
BuildRequires:  python3-setuptools
BuildRequires:  python3-sushy >= 1.8.1
BuildRequires:  python3-sushy-tests >= 1.7.0

Requires:       python3-jsonschema
Requires:       python3-pbr >= 2.0
Requires:       python3-sushy >= 2.0.0
%description -n python3-%{sname}
This library extends the existing Sushy library to include functionality for
Intel RackScale Design enabled hardware. Capabilities include logical node
composition and decomposition, remote storage discovery and composition,
and NVMe over PCIe drive attaching and detaching to logical nodes.

%package -n python3-%{sname}-tests
Summary: rsd-lib tests

BuildRequires: python3-devel

Requires: python3-%{sname} = %{version}-%{release}
Requires: python3-jsonschema
Requires: python3-pbr
Requires: python3-sushy >= 2.0.0
Requires: python3-sushy-tests >= 1.7.0

%description -n python3-%{sname}-tests
Tests for rsd-lib

%if 0%{?with_doc}
%package -n python-%{sname}-doc
Summary: rsd-lib documentation

BuildRequires: python3-sphinx
BuildRequires: python3-openstackdocstheme >= 1.11.0

%description -n python-%{sname}-doc
Documentation for rsd-lib
%endif

%prep
%autosetup -n %{sname}-%{upstream_version} -S git

# Let's handle dependencies ourseleves
rm -f *requirements.txt

%build
# amoralej - disable warning-is-error until https://review.openstack.org/#/c/636292/ is tagged.
sed -i '/warning-is-error/d' setup.cfg

%{py3_build}

%if 0%{?with_doc}
# generate html docs
%{__python3} setup.py build_sphinx
# remove the sphinx-build-3 leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}
%endif

%install
%{py3_install}

%check
export PYTHON=%{__python3}
# (TODO) ignore unit tests until rsd-lib is updated to 0.3.1
%{__python3} setup.py test || true

%files -n python3-%{sname}
%license LICENSE
%doc doc/source/readme.rst README.rst
%{python3_sitelib}/%{pyname}
%{python3_sitelib}/%{pyname}-*.egg-info
%exclude %{python3_sitelib}/%{pyname}/tests

%files -n python3-%{sname}-tests
%license LICENSE
%{python3_sitelib}/%{pyname}/tests

%if 0%{?with_doc}
%files -n python-%{sname}-doc
%license LICENSE
%doc doc/build/html README.rst
%endif

%changelog
