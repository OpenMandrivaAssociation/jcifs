%{?_javapackages_macros:%_javapackages_macros}
Name:          jcifs
Version:       1.3.18
Release:       5%{?dist}
Summary:       Common Internet File System Client in 100% Java
# Licenses:
#   src/jcifs/util/DES.java: BSD and MIT
#   src/jcifs/util/MD4.java: BSD
#   all the rest:            LGPLv2+
License:       LGPLv2+ and BSD and MIT
URL:           https://jcifs.samba.org/
Source0:       http://jcifs.samba.org/src/%{name}-%{version}.tgz
Source1:       http://mirrors.ibiblio.org/pub/mirrors/maven2/jcifs/jcifs/1.3.17/jcifs-1.3.17.pom 
# fix javac executable
Patch0:        %{name}-1.3.17-build.patch
BuildRequires: ant
BuildRequires: javapackages-local
BuildRequires: mvn(javax.servlet:javax.servlet-api)
BuildArch:     noarch

%description
The jCIFS SMB client library enables any Java application to remotely
access shared files and directories on SMB file servers (i.e. a
Microsoft Windows "share") in addition to domain, workgroup, and
server enumeration of NetBIOS over TCP/IP networks. It is an advanced
implementation of the CIFS protocol supporting Unicode, batching,
multiplexing of threaded callers, encrypted authentication,
transactions, the Remote Access Protocol (RAP), and much more. It is
licensed under LGPL which means commercial organizations can
legitimately use it with their proprietary code(you just can't sell or
give away a modified binary only version of the library itself without
reciprocation).

%package javadoc
Summary:       Javadoc for %{name}
# Neither DES.java nor MD4.java (see License comment) are documented here
License:       LGPLv2+

%description javadoc
This package contains the API documentation for %{name}.

%package demo
Summary:       Demo for %{name}
# Files from the directory 'examples' are here, some are under GPLv2+
License:       LGPLv2+ and GPLv2+
Requires:      %{name} = %{version}-%{release}

%description demo
Demonstrations and samples for %{name}.

%prep
%setup -q -n %{name}_%{version}
find -name '*.class' -delete
find -name '*.jar' -delete
%patch0 -p0
sed -i "s|1.5|1.6|" build.xml
cp -p %{SOURCE1} pom.xml
sed -i "s|<version>1.3.17|<version>%{version}|" pom.xml
%pom_remove_plugin :maven-gpg-plugin

%pom_xpath_set "pom:dependency[pom:groupId = 'javax.servlet']/pom:version" 3.1.0
%pom_xpath_set "pom:dependency[pom:groupId = 'javax.servlet']/pom:artifactId" javax.servlet-api

%mvn_file %{name}:%{name} %{name}
%mvn_alias %{name}:%{name} org.samba.jcifs:jcifs

%build

export CLASSPATH=$(build-classpath glassfish-servlet-api)
export OPT_JAR_LIST=:
%ant jar javadoc docs

%mvn_artifact pom.xml %{name}-%{version}.jar

%install
%mvn_install -J docs/api

mkdir -p %{buildroot}%{_datadir}/%{name}/examples
cp -pr examples/*.java  %{buildroot}%{_datadir}/%{name}/examples

%files -f .mfiles
%doc README.txt docs/*.{html,txt,gif}
%doc LICENSE.txt

%files javadoc -f .mfiles-javadoc
%doc LICENSE.txt

%files demo
%{_datadir}/%{name}/*
%doc LICENSE.txt

%changelog
* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.18-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.18-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.18-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Feb 06 2015 gil cattaneo <puntogil@libero.it> 1.3.18-2
- introduce license macro

* Sat Nov 01 2014 gil cattaneo <puntogil@libero.it> 1.3.18-1
- update to 1.3.18

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.17-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Mar 04 2014 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.3.17-11
- Use Requires: java-headless rebuild (#1067528)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.17-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jul 23 2013 Tomas Radej <tradej@redhat.com> - 1.3.17-9
- Fixed license tags

* Fri Jun 14 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.3.17-8
- Update to current packaging guidelines

* Fri Feb 08 2013 Jon Ciesla <limburgher@gmail.com> 1.3.17-7
- Rebuild to get update to mirror due to tagging issue,
- see https://fedorahosted.org/rel-eng/ticket/5467

* Fri Nov 16 2012 gil cattaneo <puntogil@libero.it> 1.3.17-6
- rebuilt

* Mon Nov 12 2012 gil cattaneo <puntogil@libero.it> 1.3.17-5
- fixed rhbz#875685 (Incorrect license tag)

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.17-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Apr 18 2012 gil cattaneo <puntogil@libero.it> 1.3.17-3
- remove maven build method
- clean spec file

* Wed Apr 18 2012 gil cattaneo <puntogil@libero.it> 1.3.17-2
- fixed license field
- add LICENSE.txt file to main package and subpackages
- add Requires: jpackage-utils to javadoc subpackage

* Sun Mar 25 2012 gil cattaneo <puntogil@libero.it> 1.3.17-1
- initial rpm
