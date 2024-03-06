export TERM=xterm-256color
export CLICOLOR_FORCE=true
export RICHGO_FORCE_COLOR=1

default: prepare-go install-go build-go

#prepare:
#	@ echo "###" && echo "### Preparando o ambiente local:" && echo "###" && echo#
#	#@ wget https://dl.google.com/go/go1.17.7.linux-amd64.tar.gz
#	#@ rm -rf /usr/local/go && tar -C /usr/local -xzf go1.17.7.linux-amd64.tar.gz 
#	@ echo "export PATH=\$PATH:/usr/local/go/bin" >> ~/.profile
#	@ echo "###" && echo "### Verificando a versão do Go instalada::" && echo "###" && echo
#	@ go version

prepare-go:
	@ echo "###"; echo "### Preparando arquivo go.mod"; echo "###"
	@ if [ ! -f "backend/go.mod" ] ; then go mod init bitbucket.org/bexstech/bexs-devops-exam; fi
	@ if [ -f "go.mod" ] ; then mv go.mod backend/; fi

install-go:
	@ echo
	@ echo "###"; echo "### Instalando dependências"; echo "###"
	@ cd backend/ && go mod tidy && cd ..

build-go:
	@ echo
	@ echo "###"; echo "### Gerando binário"; echo "###"
	@ cd backend/ && CGO_ENABLED=1 CC=gcc GOOS=linux go build -o bin/service cmd/main.go && cd ..

docker:
	@ docker-compose up -d

#setup-local: install
#	@go get -u golang.org/x/tools/...
#	@go get -u golang.org/x/lint/golint
#	@go get -u github.com/haya14busa/goverage
#	@go get -u github.com/kyoh86/richgo
#	@go get github.com/joho/godotenv/cmd/godotenv
#	@curl -sfL https://install.goreleaser.com/github.com/golangci/golangci-lint.sh | sh -s -- -b $(GOPATH)/bin v1.15.0
#	@golangci-lint --version


test: install test-lint test-coverage

test-coverage:
	@echo "### Run tests..."
	@richgo test -failfast -coverprofile=coverage.out ./...
	@go tool cover -html=coverage.out -o coverage.html

test-lint:
	@golangci-lint run

clean:
	@go clean -modcache
