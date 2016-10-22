%{?scl:%scl_package perl-Software-License}

# We need to patch the test suite if we have an old version of Test::More
%global old_test_more %(%{?scl:scl enable %{scl} '}perl -MTest::More -e %{?scl:'"}'%{?scl:"'}print (($Test::More::VERSION < 0.88) ? 1 : 0);%{?scl:'"}'%{?scl:"'} 2>/dev/null || echo 0%{?scl:'})

Name:           %{?scl_prefix}perl-Software-License
Version:        0.103012
Release:        4%{?dist}
Summary:        Package that provides templated software licenses
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/Software-License/
Source0:        http://search.cpan.org/CPAN/authors/id/R/RJ/RJBS/Software-License-%{version}.tar.gz
Patch1:         Software-License-0.103012-old-Test::More.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(id -nu)
BuildArch:      noarch
# Module Build
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  %{?scl_prefix}perl
BuildRequires:  %{?scl_prefix}perl-generators
BuildRequires:  %{?scl_prefix}perl(ExtUtils::MakeMaker)
# Module Runtime
BuildRequires:  %{?scl_prefix}perl(Carp)
BuildRequires:  %{?scl_prefix}perl(Data::Section)
BuildRequires:  %{?scl_prefix}perl(File::Spec)
BuildRequires:  %{?scl_prefix}perl(IO::Dir)
BuildRequires:  %{?scl_prefix}perl(Module::Load)
BuildRequires:  %{?scl_prefix}perl(parent)
BuildRequires:  %{?scl_prefix}perl(strict)
BuildRequires:  %{?scl_prefix}perl(Text::Template)
BuildRequires:  %{?scl_prefix}perl(warnings)
# Test Suite
BuildRequires:  %{?scl_prefix}perl(File::Spec)
BuildRequires:  %{?scl_prefix}perl(Test::More)
%if !%{defined perl_small}
BuildRequires:  %{?scl_prefix}perl(Test::Pod)
%endif
BuildRequires:  %{?scl_prefix}perl(Try::Tiny)
# Optional Tests
%if 0%{!?perl_bootstrap:1} && !%{defined perl_small}
BuildRequires:  %{?scl_prefix}perl(CPAN::Meta) >= 2.120900
BuildRequires:  %{?scl_prefix}perl(Software::License::CCpack)
%endif
# Runtime
Requires:       %{?scl_prefix}perl(:MODULE_COMPAT_%(%{?scl:scl enable %{scl} '}eval "$(perl -V:version)";echo $version%{?scl:'}))

%description
Software-License contains templates for common open source software licenses.

%prep
%setup -q -n Software-License-%{version}

# Compatibility with old Test::More versions
%if %{old_test_more}
%patch1
%endif

%build
%{?scl:scl enable %{scl} '}perl Makefile.PL INSTALLDIRS=vendor && make %{?_smp_mflags}%{?scl:'}

%install
rm -rf %{buildroot}
%{?scl:scl enable %{scl} '}make pure_install DESTDIR=%{buildroot}%{?scl:'}
find %{buildroot} -type f -name .packlist -delete
%{_fixperms} %{buildroot}

%check
%{?scl:scl enable %{scl} '}make test%{?scl:'}
%if !%{defined perl_small}
%{?scl:scl enable %{scl} '}make test TEST_FILES="$(echo $(find xt/ -name %{?scl:'"}'%{?scl:"'}*.t%{?scl:'"}'%{?scl:"'}))"%{?scl:'}
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%if 0%{?_licensedir:1}
%doc LICENSE
%else
%doc LICENSE
%endif
%doc Changes README
%{perl_vendorlib}/Software/
%{_mandir}/man3/Software::License.3*
%{_mandir}/man3/Software::License::*.3*
%{_mandir}/man3/Software::LicenseUtils.3*

%changelog
* Tue Jul 19 2016 Petr Pisar <ppisar@redhat.com> - 0.103012-4
- SCL

* Wed May 18 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.103012-3
- Perl 5.24 re-rebuild of bootstrapped packages

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.103012-2
- Perl 5.24 rebuild

* Sun Apr 24 2016 Paul Howarth <paul@city-fan.org> - 0.103012-1
- Update to 0.103012
  - Consider license names without parentheses when scanning text for license
  - When scanning text for license, put known substrings inside \b..\b
- Simplify find command using -delete
- Update patch for building with old Test::More versions

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.103011-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sun Jan 17 2016 Paul Howarth <paul@city-fan.org> - 0.103011-1
- Update to 0.103011
  - Do not load Sub::Install, since it isn't used!
  - Eliminate superfluous FULL STOP characters (".")
- Update patch for building with old Test::More versions
- Classify buildreqs by usage
- Use %%doc where possible

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.103010-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 06 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.103010-4
- Perl 5.22 rebuild

* Fri Aug 29 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.103010-3
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.103010-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Mar 30 2014 Paul Howarth <paul@city-fan.org> - 0.103010-1
- Update to 0.103010
  - Fix guess_license_from_pod's return on GPL licenses
- Update patch for building with old Test::More versions

* Fri Feb 21 2014 Paul Howarth <paul@city-fan.org> - 0.103009-1
- Update to 0.103009
  - Updated FSF mailing address in license text for GFDL version 1.2, GPL
    versions 1 and 2, and LGPL 2.1
- Update patch for building with old Test::More versions
- Don't try to run the extra tests with EL-5 or EL-6

* Sun Nov 17 2013 Paul Howarth <paul@city-fan.org> - 0.103008-1
- Update to 0.103008
  - Faster!
  - Add new_from_short_name to LicenseUtils for spdx.org-style short names
  - Avoid double trailing dots in expanded licenses
  - Fix some errors in (3-clause) BSD license text
  - The 2-clause BSD ("FreeBSD") license no longer incorrectly puts "FreeBSD"
    as the owner in the license full text
- Update patch for building with old Test::More versions

* Sun Oct 27 2013 Paul Howarth <paul@city-fan.org> - 0.103007-1
- Update to 0.103007
  - Fix regex to allow guessing from meta things like perl_5
  - Replace 'use base' with 'use parent'
- BR: perl(Try::Tiny) for the test suite
- Update patch for building with old Test::More versions

* Mon Oct 21 2013 Paul Howarth <paul@city-fan.org> - 0.103006-2
- Update patch for building with old Test::More versions
- Update core buildreqs for completeness

* Mon Oct 21 2013 Daniel P. Berrange <berrange@redhat.com> - 0.103006-1
* Update to 0.103006 release (rhbz #1021385)

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.103005-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jul 22 2013 Petr Pisar <ppisar@redhat.com> - 0.103005-3
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.103005-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Dec  8 2012 Paul Howarth <paul@city-fan.org> - 0.103005-1
- Update to 0.103005
  - Add MPL 2.0
- BR: perl(File::Temp)
- Release tests moved to xt/
- Update patch for building with old Test::More versions

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.103004-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jun 14 2012 Petr Pisar <ppisar@redhat.com> - 0.103004-3
- Perl 5.16 rebuild

* Wed Mar  7 2012 Paul Howarth <paul@city-fan.org> - 0.103004-2
- Add test suite patch to support building with Test::More < 0.88 so that we
  can build for EPEL-5, only applying the patch when necessary
- Drop redundant versioned requirements of XXX >= 0.000
- Drop BR: perl ≥ 1:5.6.0; even EL-3 could have satisfied that
- BR: perl(base) and perl(Carp), which could be dual-lived
- BR: perl(Test::Pod) for full test coverage
- Run the release tests too
- Don't need to remove empty directories from buildroot
- Don't use macros for commands
- Use DESTDIR rather than PERL_INSTALL_ROOT
- Drop %%defattr, redundant since rpm 4.4
- Make %%files list more explicit

* Mon Jan 30 2012 Daniel P. Berrange <berrange@redhat.com> - 0.103004-1
- Update to 0.103004 release (rhbz #750790)

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.103002-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sat Sep 03 2011 Iain Arnell <iarnell@gmail.com> 0.103002-1
- update to latest upstream version

* Wed Jun 29 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.102341-4
- Perl mass rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.102341-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 22 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.102341-2
- 661697 rebuild for fixing problems with vendorach/lib

* Fri Dec 17 2010 Daniel P. Berrange <berrange@redhat.com> - 0.102341-1
- Update to 0.102341 release

* Wed Jun 02 2010 Iain Arnell <iarnell@gmail.com> 0.101410-1
- update to 0.101410 release

* Thu May 06 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.012-4
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.012-3
- rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.012-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jul 22 2009 Daniel P. Berrange <berrange@redhat.com> - 0.012-1
- Update to 0.012 release

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.008-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Sep 20 2008 Daniel P. Berrange <berrange@redhat.com> 0.008-3
- Remove explicit requires that duplicate automatic perl deps

* Sat Sep 06 2008 Daniel P. Berrange <berrange@redhat.com> 0.008-2
- Fix description
- Add missing Test::More BR

* Fri Sep 05 2008 Daniel P. Berrange <berrange@redhat.com> 0.008-1
- Specfile autogenerated by cpanspec 1.77.
