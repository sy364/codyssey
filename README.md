# 개발 워크스테이션 구축 미션

## 1. 프로젝트 개요
* **목표:** 터미널 환경 제어, Docker를 활용한 컨테이너 기반 실행 환경 구축 및 Git/GitHub를 통한 버전 관리 경험.
* **주요 내용:** 리눅스 CLI 조작, 커스텀 컨테이너 이미지 빌드 및 실행, 포트 매핑과 볼륨 마운트 검증.

## 2. 실행 환경
* **OS:** macOS (Apple Silicon M1)
* **Shell / Terminal:** zsh
* **Docker 버전:** (OrbStack 설치 후 기입 예정)
* **Git 버전:** (git --version 결과 기입)

## 3. 수행 항목 체크리스트
- [x] 터미널 기본 명령어 실습
- [x] 파일 및 디렉토리 권한 제어 실습
- [x] Docker 데몬 설치 및 기본 동작 점검
- [x] Dockerfile 기반 커스텀 이미지 제작
- [x] 포트 매핑 및 브라우저 접속 검증
- [x] 바인드 마운트 및 볼륨 영속성 검증
- [x] Git 사용자 설정 및 GitHub 저장소 연동

## 4. 터미널 조작 및 권한 실습 로그

### 4.1 터미널 기본 조작 (생성, 확인 등)
**검증 방법:** `vi`, `mkdir` 명령어로 파일과 폴더를 생성하고 `ls -al`로 확인.

```bash
# 명령어 및 출력 결과 기입
kimseyun@gimseyun-ui-MacBookPro ~ % git clone [https://github.com/sy364/codyssey.git](https://github.com/sy364/codyssey.git)
'codyssey'에 복제합니다...
warning: 빈 저장소를 복제한 것처럼 보입니다.
kimseyun@gimseyun-ui-MacBookPro ~ % cd codyssey
kimseyun@gimseyun-ui-MacBookPro codyssey % git config --list
credential.helper=osxkeychain
user.name=sy364
user.email=seyoon0604@gmail.com
core.repositoryformatversion=0
core.filemode=true
core.bare=false
core.logallrefupdates=true
core.ignorecase=true
core.precomposeunicode=true
remote.origin.url=[https://github.com/sy364/codyssey.git](https://github.com/sy364/codyssey.git)
remote.origin.fetch=+refs/heads/*:refs/remotes/origin/*
branch.main.remote=origin
branch.main.merge=refs/heads/main
kimseyun@gimseyun-ui-MacBookPro codyssey % vi README.md
kimseyun@gimseyun-ui-MacBookPro codyssey % mkdir test_dir
kimseyun@gimseyun-ui-MacBookPro codyssey % vi test_dir/test.txt
kimseyun@gimseyun-ui-MacBookPro codyssey % ls -al
total 0
drwxr-xr-x   5 kimseyun  staff   160  7 28 20:38 .
drwxr-x---+ 62 kimseyun  staff  1984  7 28 20:38 ..
drwxr-xr-x   9 kimseyun  staff   288  7 28 20:32 .git
-rw-r--r--   1 kimseyun  staff     0  7 28 20:37 README.md
drwxr-xr-x   3 kimseyun  staff    96  7 28 20:38 test_dir
kimseyun@gimseyun-ui-MacBookPro codyssey % chmod 755 test_dir
kimseyun@gimseyun-ui-MacBookPro codyssey % chmod 644 test_dir/test.txt 
kimseyun@gimseyun-ui-MacBookPro codyssey % ls -al
total 0
drwxr-xr-x   5 kimseyun  staff   160  7 28 20:38 .
drwxr-x---+ 62 kimseyun  staff  1984  7 28 20:38 ..
drwxr-xr-x   9 kimseyun  staff   288  7 28 20:32 .git
-rw-r--r--   1 kimseyun  staff     0  7 28 20:37 README.md
drwxr-xr-x   3 kimseyun  staff    96  7 28 20:38 test_dir
kimseyun@gimseyun-ui-MacBookPro codyssey % ls -al test_dir
total 0
drwxr-xr-x  3 kimseyun  staff   96  7 28 20:38 .
drwxr-xr-x  5 kimseyun  staff  160  7 28 20:38 ..
-rw-r--r--  1 kimseyun  staff    0  7 28 20:38 test.txt
kimseyun@gimseyun-ui-MacBookPro codyssey % pwd
/Users/kimseyun/codyssey
kimseyun@gimseyun-ui-MacBookPro codyssey % cp test_dir/test.txt test_dir/copy.txt  
kimseyun@gimseyun-ui-MacBookPro codyssey % mv test_dir/copy.txt test_dir/rename.txt
kimseyun@gimseyun-ui-MacBookPro codyssey % cat test_dir/rename.txt 
kimseyun@gimseyun-ui-MacBookPro codyssey % rm test_dir/rename.txt 
kimseyun@gimseyun-ui-MacBookPro codyssey % ls
README.md	test_dir
```

## 5. Docker 설치 및 기본 점검
**검증 방법:** 'docker --version'과 'docker info' 명령어로 설치

```bash
kimseyun@gimseyun-ui-MacBookPro codyssey % docker --version
Docker version 29.4.0, build 9d7ad9f
kimseyun@gimseyun-ui-MacBookPro codyssey % docker info
Client:
 Version:    29.4.0
 Context:    orbstack
 Debug Mode: false
 Plugins:
  agent: Docker AI Agent Runner (Docker Inc.)
    Version:  v1.54.0
    Path:     /Users/kimseyun/.docker/cli-plugins/docker-agent
  ai: Docker AI Agent - Ask Gordon (Docker Inc.)
    Version:  v1.20.2
    Path:     /Users/kimseyun/.docker/cli-plugins/docker-ai
  buildx: Docker Buildx (Docker Inc.)
    Version:  v0.33.0
    Path:     /Users/kimseyun/.docker/cli-plugins/docker-buildx
  compose: Docker Compose (Docker Inc.)
    Version:  v5.1.2
    Path:     /Users/kimseyun/.docker/cli-plugins/docker-compose
  debug: Get a shell into any image or container (Docker Inc.)
    Version:  0.0.47
    Path:     /Users/kimseyun/.docker/cli-plugins/docker-debug
  desktop: Docker Desktop commands (Docker Inc.)
    Version:  v0.3.0
    Path:     /Users/kimseyun/.docker/cli-plugins/docker-desktop
  dhi: CLI for managing Docker Hardened Images (Docker Inc.)
    Version:  v0.0.3
    Path:     /Users/kimseyun/.docker/cli-plugins/docker-dhi
  extension: Manages Docker extensions (Docker Inc.)
    Version:  v0.2.31
    Path:     /Users/kimseyun/.docker/cli-plugins/docker-extension
  init: Creates Docker-related starter files for your project (Docker Inc.)
    Version:  v1.4.0
    Path:     /Users/kimseyun/.docker/cli-plugins/docker-init
  mcp: Docker MCP Plugin (Docker Inc.)
    Version:  v0.42.0
    Path:     /Users/kimseyun/.docker/cli-plugins/docker-mcp
  model: Docker Model Runner (Docker Inc.)
    Version:  v1.1.37
    Path:     /Users/kimseyun/.docker/cli-plugins/docker-model
  offload: Docker Offload (Docker Inc.)
    Version:  v0.5.85
    Path:     /Users/kimseyun/.docker/cli-plugins/docker-offload
  pass: Docker Pass Secrets Manager Plugin (beta) (Docker Inc.)
    Version:  v0.0.25
    Path:     /Users/kimseyun/.docker/cli-plugins/docker-pass
  sandbox: Docker Sandbox (Docker Inc.)
    Version:  v0.12.0
    Path:     /Users/kimseyun/.docker/cli-plugins/docker-sandbox
  sbom: View the packaged-based Software Bill Of Materials (SBOM) for an image (Anchore Inc.)
    Version:  0.6.0
    Path:     /Users/kimseyun/.docker/cli-plugins/docker-sbom
  scout: Docker Scout (Docker Inc.)
    Version:  v1.20.4
    Path:     /Users/kimseyun/.docker/cli-plugins/docker-scout

Server:
 Containers: 0
  Running: 0
  Paused: 0
  Stopped: 0
 Images: 0
 Server Version: 29.4.0
 Storage Driver: overlayfs
  driver-type: io.containerd.snapshotter.v1
 Logging Driver: json-file
 Cgroup Driver: cgroupfs
 Cgroup Version: 2
 Plugins:
  Volume: local
  Network: bridge host ipvlan macvlan null overlay
  Log: awslogs fluentd gcplogs gelf journald json-file local splunk syslog
 CDI spec directories:
  /etc/cdi
  /var/run/cdi
 Swarm: inactive
 Runtimes: io.containerd.runc.v2 runc
 Default Runtime: runc
 Init Binary: docker-init
 containerd version: 301b2dac98f15c27117da5c8af12118a041a31d9
 runc version: c241c0bb5e60a8e8c1b2e53d4eca8d0068d8d57e
 init version: de40ad0
 Security Options:
  seccomp
   Profile: builtin
  cgroupns
 Kernel Version: 7.0.11-orbstack-00360-gc9bc4d96ac70
 Operating System: OrbStack
 OSType: linux
 Architecture: aarch64
 CPUs: 8
 Total Memory: 7.818GiB
 Name: orbstack
 ID: 27ad8d19-469a-4857-92d5-7e697e735d29
 Docker Root Dir: /var/lib/docker
 Debug Mode: false
 HTTP Proxy: [http://proxy.orb.internal:8305](http://proxy.orb.internal:8305)
 HTTPS Proxy: [http://proxy.orb.internal:8305](http://proxy.orb.internal:8305)
 No Proxy: localhost,127.0.0.1,127.0.0.0/8,::1,10.0.0.0/8,172.16.0.0/12,192.168.0.0/16,0.250.250.0/24,*.orb.internal,*.local,gateway.docker.internal,host.internal,host.docker.internal,host.lima.internal,docker.for.mac.localhost,docker.for.mac.host.internal
 Experimental: true
 Insecure Registries:
  ::1/128
  127.0.0.0/8
 Live Restore Enabled: false
 Product License: Community Engine
 Default Address Pools:
   Base: 192.168.97.0/24, Size: 24
   Base: 192.168.107.0/24, Size: 24
   Base: 192.168.117.0/24, Size: 24
   Base: 192.168.147.0/24, Size: 24
   Base: 192.168.148.0/24, Size: 24
   Base: 192.168.155.0/24, Size: 24
   Base: 192.168.156.0/24, Size: 24
   Base: 192.168.158.0/24, Size: 24
   Base: 192.168.163.0/24, Size: 24
   Base: 192.168.164.0/24, Size: 24
   Base: 192.168.165.0/24, Size: 24
   Base: 192.168.166.0/24, Size: 24
   Base: 192.168.167.0/24, Size: 24
   Base: 192.168.171.0/24, Size: 24
   Base: 192.168.172.0/24, Size: 24
   Base: 192.168.181.0/24, Size: 24
   Base: 192.168.183.0/24, Size: 24
   Base: 192.168.186.0/24, Size: 24
   Base: 192.168.207.0/24, Size: 24
   Base: 192.168.214.0/24, Size: 24
   Base: 192.168.215.0/24, Size: 24
   Base: 192.168.216.0/24, Size: 24
   Base: 192.168.223.0/24, Size: 24
   Base: 192.168.227.0/24, Size: 24
   Base: 192.168.228.0/24, Size: 24
   Base: 192.168.229.0/24, Size: 24
   Base: 192.168.237.0/24, Size: 24
   Base: 192.168.239.0/24, Size: 24
   Base: 192.168.242.0/24, Size: 24
   Base: 192.168.247.0/24, Size: 24
   Base: fd07:b51a:cc66:d000::/56, Size: 64
 Firewall Backend: iptables

WARNING: DOCKER_INSECURE_NO_IPTABLES_RAW is set
```

## 6. Docker 기본 운영 명령 수행
```bash
kimseyun@gimseyun-ui-MacBookPro codyssey % docker pull nginx
Using default tag: latest
latest: Pulling from library/nginx
9f270a0f328f: Pull complete 
59f54fbcd984: Pull complete 
54c3b3bebc0a: Pull complete 
9b1a2f3b8553: Pull complete 
627a5a63361a: Pull complete 
4cca0d328dc5: Pull complete 
94f27359a4c8: Pull complete 
d07ed3315b0d: Download complete 
52efd73ccaa6: Download complete 
Digest: sha256:5a88c9c45479443d7be2eadc894b4ed0a9801bae03d97a5760ae13b5c2005942
Status: Downloaded newer image for nginx:latest
docker.io/library/nginx:latest

What's next:
    View a summary of image vulnerabilities and recommendations → docker scout quickview nginx
kimseyun@gimseyun-ui-MacBookPro codyssey % docker images
                                                                i Info →   U  In Use
IMAGE          ID             DISK USAGE   CONTENT SIZE   EXTRA
nginx:latest   5a88c9c45479        258MB         64.3MB        
kimseyun@gimseyun-ui-MacBookPro codyssey % docker run -d --name test-nginx nginx
64221f675a5eb008a5ec91fc904b1e4d156d6148320e447580dd7b0b94e2fa57
kimseyun@gimseyun-ui-MacBookPro codyssey % docker ps
CONTAINER ID   IMAGE     COMMAND                   CREATED         STATUS         PORTS     NAMES
64221f675a5e   nginx     "/docker-entrypoint.…"   3 seconds ago   Up 2 seconds   80/tcp    test-nginx
kimseyun@gimseyun-ui-MacBookPro codyssey % docker logs test-nginx
/docker-entrypoint.sh: /docker-entrypoint.d/ is not empty, will attempt to perform configuration
/docker-entrypoint.sh: Looking for shell scripts in /docker-entrypoint.d/
/docker-entrypoint.sh: Launching /docker-entrypoint.d/10-listen-on-ipv6-by-default.sh
10-listen-on-ipv6-by-default.sh: info: Getting the checksum of /etc/nginx/conf.d/default.conf
10-listen-on-ipv6-by-default.sh: info: Enabled listen on IPv6 in /etc/nginx/conf.d/default.conf
/docker-entrypoint.sh: Sourcing /docker-entrypoint.d/15-local-resolvers.envsh
/docker-entrypoint.sh: Launching /docker-entrypoint.d/20-envsubst-on-templates.sh
/docker-entrypoint.sh: Launching /docker-entrypoint.d/30-tune-worker-processes.sh
/docker-entrypoint.sh: Configuration complete; ready for start up
2026/07/28 12:31:15 [notice] 1#1: using the "epoll" event method
2026/07/28 12:31:15 [notice] 1#1: nginx/1.31.3
2026/07/28 12:31:15 [notice] 1#1: built by gcc 14.2.0 (Debian 14.2.0-19) 
2026/07/28 12:31:15 [notice] 1#1: OS: Linux 7.0.11-orbstack-00360-gc9bc4d96ac70
2026/07/28 12:31:15 [notice] 1#1: getrlimit(RLIMIT_NOFILE): 20480:1048576
2026/07/28 12:31:15 [notice] 1#1: start worker processes
2026/07/28 12:31:15 [notice] 1#1: start worker process 29
2026/07/28 12:31:15 [notice] 1#1: start worker process 30
2026/07/28 12:31:15 [notice] 1#1: start worker process 31
2026/07/28 12:31:15 [notice] 1#1: start worker process 32
2026/07/28 12:31:15 [notice] 1#1: start worker process 33
2026/07/28 12:31:15 [notice] 1#1: start worker process 34
2026/07/28 12:31:15 [notice] 1#1: start worker process 35
2026/07/28 12:31:15 [notice] 1#1: start worker process 36
kimseyun@gimseyun-ui-MacBookPro codyssey % docker ps
CONTAINER ID   IMAGE     COMMAND                   CREATED          STATUS          PORTS     NAMES
64221f675a5e   nginx     "/docker-entrypoint.…"   28 minutes ago   Up 28 minutes   80/tcp    test-nginx
kimseyun@gimseyun-ui-MacBookPro codyssey % docker logs test-nginx 
/docker-entrypoint.sh: /docker-entrypoint.d/ is not empty, will attempt to perform configuration
/docker-entrypoint.sh: Looking for shell scripts in /docker-entrypoint.d/
/docker-entrypoint.sh: Launching /docker-entrypoint.d/10-listen-on-ipv6-by-default.sh
10-listen-on-ipv6-by-default.sh: info: Getting the checksum of /etc/nginx/conf.d/default.conf
10-listen-on-ipv6-by-default.sh: info: Enabled listen on IPv6 in /etc/nginx/conf.d/default.conf
/docker-entrypoint.sh: Sourcing /docker-entrypoint.d/15-local-resolvers.envsh
/docker-entrypoint.sh: Launching /docker-entrypoint.d/20-envsubst-on-templates.sh
/docker-entrypoint.sh: Launching /docker-entrypoint.d/30-tune-worker-processes.sh
/docker-entrypoint.sh: Configuration complete; ready for start up
2026/07/28 12:31:15 [notice] 1#1: using the "epoll" event method
2026/07/28 12:31:15 [notice] 1#1: nginx/1.31.3
2026/07/28 12:31:15 [notice] 1#1: built by gcc 14.2.0 (Debian 14.2.0-19) 
2026/07/28 12:31:15 [notice] 1#1: OS: Linux 7.0.11-orbstack-00360-gc9bc4d96ac70
2026/07/28 12:31:15 [notice] 1#1: getrlimit(RLIMIT_NOFILE): 20480:1048576
2026/07/28 12:31:15 [notice] 1#1: start worker processes
2026/07/28 12:31:15 [notice] 1#1: start worker process 29
2026/07/28 12:31:15 [notice] 1#1: start worker process 30
2026/07/28 12:31:15 [notice] 1#1: start worker process 31
2026/07/28 12:31:15 [notice] 1#1: start worker process 32
2026/07/28 12:31:15 [notice] 1#1: start worker process 33
2026/07/28 12:31:15 [notice] 1#1: start worker process 34
2026/07/28 12:31:15 [notice] 1#1: start worker process 35
2026/07/28 12:31:15 [notice] 1#1: start worker process 36
kimseyun@gimseyun-ui-MacBookPro codyssey % docker stats --no-stream
CONTAINER ID   NAME         CPU %     MEM USAGE / LIMIT     MEM %     NET I/O         BLOCK I/O         PIDS
64221f675a5e   test-nginx   0.00%     7.762MiB / 7.818GiB   0.10%     1.66kB / 126B   15.8MB / 8.19kB   9
kimseyun@gimseyun-ui-MacBookPro codyssey % docker stop test-nginx 
test-nginx
```

## 7. 컨테이너 실행 실습
```bash
kimseyun@gimseyun-ui-MacBookPro codyssey % docker run hello-world

Hello from Docker!
This message shows that your installation appears to be working correctly.

To generate this message, Docker took the following steps:
 1. The Docker client contacted the Docker daemon.
 2. The Docker daemon pulled the "hello-world" image from the Docker Hub.
    (arm64v8)
 3. The Docker daemon created a new container from that image which runs the
    executable that produces the output you are currently reading.
 4. The Docker daemon streamed that output to the Docker client, which sent it
    to your terminal.

To try something more ambitious, you can run an Ubuntu container with:
 $ docker run -it ubuntu bash

Share images, automate workflows, and more with a free Docker ID:
 [https://hub.docker.com/](https://hub.docker.com/)

For more examples and ideas, visit:
 [https://docs.docker.com/get-started/](https://docs.docker.com/get-started/)

kimseyun@gimseyun-ui-MacBookPro codyssey % docker run -it ubuntu bash
Unable to find image 'ubuntu:latest' locally
latest: Pulling from library/ubuntu
693710ba2039: Pull complete 
55237ac9880d: Pull complete 
fdfb14aa961e: Download complete 
Digest: sha256:3131b4cc82a783df6c9df078f86e01819a13594b865c2cad47bd1bca2b7063bb
Status: Downloaded newer image for ubuntu:latest
root@2f00464a02af:/# 
root@2f00464a02af:/# ls
bin   dev  home  media  opt   root  sbin  sys  usr
boot  etc  lib   mnt    proc  run   srv   tmp  var
root@2f00464a02af:/# echo "hello from ubuntu"
hello from ubuntu
root@2f00464a02af:/# exit
exit
```
**attach와 exec 차이점**
* **attach**: 컨테이너의 메인 프로세스(PID1)에 현재 터미널을 직접 연결한다. 접속 상태에서 종료(exit) 시 메인 프로세스가 함께 종료되므로 컨테이너 전체가 멈춘다.
* **exec**: 이미 백그라운드에서 실행 중인 컨테이너 환경 내부에 새로운 별도 프로세스(쉘 등)를 생성해 접속한다. 작업을 마치고 exit로 빠져나와도 해당 쉘만 종료되며, 컨테이너의 원래 메인 프로세스는 계속 실행 상태를 유지한다.

## 8. 기존 Dockerfile 기반 커스텀 이미지 제작 및 포트 매핑

**1. 선택한 베이스 이미지**
* (A) 웹 서버 베이스 이미지 활용 (`nginx:latest`)

**2. 커스텀 포인트 및 목적**
* **커스텀 포인트:** Dockerfile의 `COPY` 명령어를 사용하여 로컬에 생성한 `index.html` 파일을 컨테이너 내부 NGINX의 기본 서비스 경로(`/usr/share/nginx/html/index.html`)로 덮어씌움.
* **목적:** 기존 NGINX 웹 서버의 통신 기능은 유지하면서, 접속 시 출력되는 화면을 사용자가 직접 작성한 정적 웹페이지(Hello Codyssey Custom Image)로 교체하여 서비스하기 위함.

**3. 빌드/실행 명령 및 접속 증거 로그**

```bash
# 1. 정적 콘텐츠 파일 생성 및 Dockerfile 작성
kimseyun@gimseyun-ui-MacBookPro codyssey % echo "<h1>Hello Codyssey Custom Image</h1>" > index.html
kimseyun@gimseyun-ui-MacBookPro codyssey % vi Dockerfile

# 2. 커스텀 이미지 빌드
kimseyun@gimseyun-ui-MacBookPro codyssey % docker build -t my-custom-nginx .
[+] Building 0.5s (7/7) FINISHED                               docker:orbstack
 => [internal] load build definition from Dockerfile                      0.0s
 => => transferring dockerfile: 114B                                      0.0s
 => [internal] load metadata for docker.io/library/nginx:latest           0.0s
 => [internal] load .dockerignore                                         0.0s
 => => transferring context: 2B                                           0.0s
 => [internal] load build context                                         0.0s
 => => transferring context: 74B                                          0.0s
 => [1/2] FROM docker.io/library/nginx:latest@sha256:5a88c9c45479443d7be  0.1s
 => => resolve docker.io/library/nginx:latest@sha256:5a88c9c45479443d7be  0.0s
 => [2/2] COPY index.html /usr/share/nginx/html/index.html                0.0s
 => exporting to image                                                    0.1s
 => => exporting layers                                                   0.1s
 => => exporting manifest sha256:b4a1251e96b63e95626932724fd90b54a7d6508  0.0s
 => => exporting config sha256:ad309bb943f5d1921f0a015be299de7ee2bd8e438  0.0s
 => => exporting attestation manifest sha256:08670481f3aa7c263b74ccc17d5  0.0s
 => => exporting manifest list sha256:e3ddf3a411f2d6dc76c433ce17c8f68bcc  0.0s
 => => naming to docker.io/library/my-custom-nginx:latest                 0.0s
 => => unpacking to docker.io/library/my-custom-nginx:latest              0.0s

# 3. 포트 매핑을 적용한 컨테이너 실행
kimseyun@gimseyun-ui-MacBookPro codyssey % docker run -d -p 8080:80 --name my-web my-custom-nginx
4bb8fe1ce111ff8e1743fb762053e65444be423b3d18984a08c6a66c2c54585e

# 4. 포트 매핑 및 브라우저 접속 증거 (curl 응답)
kimseyun@gimseyun-ui-MacBookPro codyssey % curl http://localhost:8080
<h1>Hello Codyssey Custom Image</h1>
```

## 9. Docker 볼륨 영속성 검증

**검증 방법:** 도커 볼륨을 생성해 컨테이너 내부 경로에 마운트하여 파일을 생성한 뒤, 해당 컨테이너를 삭제하고 새로운 컨테이너에 동일한 볼륨을 연결하여 데이터가 유지됨을 확인.

**[생성/연결/검증 절차 및 출력 로그]**

```bash
# 1. 볼륨 생성 및 데이터 기록
kimseyun@gimseyun-ui-MacBookPro codyssey % docker volume create my-data
my-data
kimseyun@gimseyun-ui-MacBookPro codyssey % docker run -it --name vol-writer -v my-data:/app ubuntu bash
root@7eb714019fbe:/# echo "permanent data saved" > /app/test.txt
root@7eb714019fbe:/# cat /app/test.txt
permanent data saved
root@7eb714019fbe:/# exit
exit

# 2. 기존 컨테이너 삭제 및 확인 (vol-writer 삭제됨)
kimseyun@gimseyun-ui-MacBookPro codyssey % docker rm vol-writer
vol-writer
kimseyun@gimseyun-ui-MacBookPro codyssey % docker ps -a
CONTAINER ID   IMAGE             COMMAND                   CREATED             STATUS                         PORTS                                     NAMES
4bb8fe1ce111   my-custom-nginx   "/docker-entrypoint.…"   17 minutes ago      Up 17 minutes                  0.0.0.0:8080->80/tcp, [::]:8080->80/tcp   my-web
2f00464a02af   ubuntu            "bash"                    50 minutes ago      Exited (0) 48 minutes ago                                                interesting_shtern
6816673f2cd5   hello-world       "/hello"                  51 minutes ago      Exited (0) 51 minutes ago                                                sleepy_keller
802468e1b438   hello-world       "/hello"                  About an hour ago   Exited (0) About an hour ago                                             youthful_satoshi
64221f675a5e   nginx             "/docker-entrypoint.…"   19 hours ago        Exited (0) 19 hours ago                                                  test-nginx

# 3. 새 컨테이너로 동일한 볼륨 연결 및 데이터 생존 확인
kimseyun@gimseyun-ui-MacBookPro codyssey % docker run -it --name vol-reader -v my-data:/app ubuntu cat /app/test.txt
permanent data saved
```

## 10. Git 설정 및 GitHub 연동

**Git 사용자 설정 결과 (`git config --list`)**

```bash
kimseyun@gimseyun-ui-MacBookPro codyssey % git config --global user.name "kimseyun"
kimseyun@gimseyun-ui-MacBookPro codyssey % git config --global user.email "seyo********@gmail.com"
kimseyun@gimseyun-ui-MacBookPro codyssey % git config --global init.defaultBranch main
kimseyun@gimseyun-ui-MacBookPro codyssey % git config --list
credential.helper=osxkeychain
user.name=kimseyun
user.email=seyo********@gmail.com
init.defaultbranch=main
core.repositoryformatversion=0
core.filemode=true
core.bare=false
core.logallrefupdates=true
core.ignorecase=true
core.precomposeunicode=true
remote.origin.url=[https://github.com/sy364/codyssey.git](https://github.com/sy364/codyssey.git)
remote.origin.fetch=+refs/heads/*:refs/remotes/origin/*
branch.main.remote=origin
branch.main.merge=refs/heads/main
```