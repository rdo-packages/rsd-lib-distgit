%{!?sources_gpg: %{!?dlrn:%global sources_gpg 1} }
%global sources_gpg_sign 0xcdc08088c3cb45a9be08332b2354069e5b504663
%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
# we are excluding some BRs from automatic generator
%global excluded_brs doc8 bandit pre-commit hacking flake8-import-order
# Exclude sphinx from BRs if docs are disabled
%if ! 0%{?with_doc}
%global excluded_brs %{excluded_brs} sphinx openstackdocstheme
%endif

%global sname rsd-lib
%global pyname rsd_lib

%global with_doc 1

Name:           python-%{sname}
Version:        1.2.0
Release:        2%{?dist}
Summary:        Python library for interfacing with Intel Rack Scale Design enabled hardware.

License:        Apache-2.0
URL:            http://git.openstack.org/cgit/openstack/%{sname}
Source0:        http://tarballs.openstack.org/%{sname}/%{sname}-%{upstream_version}.tar.gz
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
Source101:        http://tarballs.openstack.org/%{sname}/%{sname}-%{upstream_version}.tar.gz.asc
Source102:        https://releases.openstack.org/_static/%{sources_gpg_sign}.txt
%endif
BuildArch:      noarch

# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
BuildRequires:  /usr/bin/gpgv2
BuildRequires:  openstack-macros
%endif

%description
This library extends the existing Sushy library to include functionality for
Intel RackScale Design enabled hardware. Capabilities include logical node
composition and decomposition, remote storage discovery and composition,
and NVMe over PCIe drive attaching and detaching to logical nodes.

%package -n     python3-%{sname}
Summary:        %{summary}

BuildRequires:  python3-devel
BuildRequires:  pyproject-rpm-macros
%description -n python3-%{sname}
This library extends the existing Sushy library to include functionality for
Intel RackScale Design enabled hardware. Capabilities include logical node
composition and decomposition, remote storage discovery and composition,
and NVMe over PCIe drive attaching and detaching to logical nodes.

%package -n python3-%{sname}-tests
Summary: rsd-lib tests

BuildRequires: python3-sushy-tests

Requires: python3-%{sname} = %{version}-%{release}
Requires: python3-jsonschema >= 2.6.0
Requires: python3-pbr >= 2.0
Requires: python3-sushy >= 2.0.0
Requires: python3-sushy-tests >= 1.7.0

%description -n python3-%{sname}-tests
Tests for rsd-lib

%if 0%{?with_doc}
%package -n python-%{sname}-doc
Summary: rsd-lib documentation

%description -n python-%{sname}-doc
Documentation for rsd-lib
%endif

%prep
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
%{gpgverify}  --keyring=%{SOURCE102} --signature=%{SOURCE101} --data=%{SOURCE0}
%endif
%autosetup -n %{sname}-%{upstream_version} -S git


sed -i /.*-c{env:.*_CONSTRAINTS_FILE.*/d tox.ini
sed -i /^minversion.*/d tox.ini
sed -i /^requires.*virtualenv.*/d tox.ini

# Exclude some bad-known BRs
for pkg in %{excluded_brs};do
for reqfile in doc/requirements.txt test-requirements.txt; do
if [ -f $reqfile ]; then
sed -i /^${pkg}.*/d $reqfile
fi
done
done
# Automatic BR generation
%generate_buildrequires
%if 0%{?with_doc}
  %pyproject_buildrequires -t -e %{default_toxenv},docs
%else
  %pyproject_buildrequires -t -e %{default_toxenv}
%endif

%build
# amoralej - disable warning-is-error until https://review.openstack.org/#/c/636292/ is tagged.
sed -i '/warning-is-error/d' setup.cfg

%pyproject_wheel

%if 0%{?with_doc}
# generate html docs
%tox -e docs
# remove the sphinx-build-3 leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}
%endif

%install
%pyproject_install

%check
# ignore unit tests as latest commit is from Sep 2019, the test code is not 
# compatible anymore with current unittest.mock
%tox -e %{default_toxenv} || true

%files -n python3-%{sname}
%license LICENSE
%doc doc/source/readme.rst README.rst
%{python3_sitelib}/%{pyname}
%{python3_sitelib}/%{pyname}-*.dist-info
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
* Fri Mar 15 2024 RDO <dev@lists.rdoproject.org> 1.2.0-2
- Rebuild 1.2.0 in Caracal

