%define gcj_support 1
%define section        free

Name:           jcifs
Version:        1.2.16
Release:        %mkrel 0.0.3
Epoch:          0
Summary:        Common Internet File System Client in 100% Java
License:        LGPL
Url:            http://jcifs.samba.org/
Group:          Development/Java
Source0:        http://jcifs.samba.org/src/jcifs-%{version}.tgz
Requires:       servlet
BuildRequires:  servlet
BuildRequires:  java-rpmbuild >= 0:1.7.2
BuildRequires:  ant >= 0:1.6.5
%if %{gcj_support}
BuildRequires:  java-gcj-compat-devel
%else
BuildRequires:  java-devel
BuildArch:      noarch
%endif

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root

%description
The jCIFS SMB client library enables any Java application to remotely
access shared files and directories on SMB file servers(i.e. a Microsoft
Windows "share") in addition to domain, workgroup, and server
enumeration of NetBIOS over TCP/IP networks. It is an advanced
implementation of the CIFS protocol supporting Unicode, batching,
multiplexing of threaded callers, encrypted authentication,
transactions, the Remote Access Protocol (RAP), and much more. It is
licensed under LGPL which means commercial organizations can
legitimately use it with their proprietary code(you just can't sell or
give away a modified binary only version of the library itself without
reciprocation).

%package javadoc
Summary:        Javadoc for %{name}
Group:          Development/Java

%description javadoc
Javadoc for %{name}.

%package demo
Summary:        Demo for %{name}
Requires:       %{name} = %{epoch}:%{version}-%{release}
Group:          Development/Java

%description demo
Demonstrations and samples for %{name}.

%prep
%setup -q -n %{name}_%{version}
# remove all binary libs
find . -name "*.jar" -exec rm -f {} \;
find . -name "*.class" -exec rm -f {} \;
rm examples/SmbTimeout.java

%build
export CLASSPATH=$(build-classpath servlet)
%{ant} jar javadoc
export CLASSPATH=$(build-classpath servlet):`pwd`/%{name}-%{version}.jar
(cd examples && %javac *.java)

%install
%{__rm} -rf %{buildroot}

# jar
mkdir -p %{buildroot}%{_javadir}
install -m 644 %{name}-%{version}.jar \
%{buildroot}%{_javadir}/%{name}-%{version}.jar
(cd %{buildroot}%{_javadir} && for jar in *-%{version}*; do \
ln -sf ${jar} ${jar/-%{version}/}; done)
# javadoc
mkdir -p $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -a docs/api/* %{buildroot}%{_javadocdir}/%{name}-%{version}
ln -s %{name}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{name} # ghost symlink

# data
mkdir -p %{buildroot}%{_datadir}/%{name}/examples
cp -a examples/*.class %{buildroot}%{_datadir}/%{name}/examples

%if %{gcj_support}
%{_bindir}/aot-compile-rpm
%endif

%clean
rm -rf %{buildroot}

%if %{gcj_support}
%post
%{update_gcjdb}

%postun
%{clean_gcjdb}
%endif

%files
%defattr(0644,root,root,0755)
%doc README.txt docs/*.{html,txt,gif}
%{_javadir}/*
%dir %{_datadir}/%{name}
%if %{gcj_support}
%dir %attr(-,root,root) %{_libdir}/gcj/%{name}
%attr(-,root,root) %{_libdir}/gcj/%{name}/%{name}-*%{version}.jar.*
%endif

%files javadoc
%defattr(0644,root,root,0755)
%{_javadocdir}/%{name}-%{version}
%{_javadocdir}/%{name}

%files demo
%defattr(0644,root,root,0755)
%{_datadir}/%{name}/examples
%if %{gcj_support}
%dir %attr(-,root,root) %{_libdir}/gcj/%{name}
%attr(-,root,root) %{_libdir}/gcj/%{name}/examples.*
%endif
