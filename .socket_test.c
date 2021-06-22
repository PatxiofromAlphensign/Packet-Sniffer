#include <stdio.h> 
#include <netdb.h>
#include <netinet/in.h>
#include<unistd.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <sys/types.h>
#define MAX 80
#define PORT 8080 // PORT being used for more than the indended purposes
#define SA struct sockaddr
#define ADDR "192.168.29.167" 

char **allocate(char **buffer, char **buffer_calloc) { // somehow adding one extra param   `char**` causes sigsev
#define size 512
	char **addrs= (char**)malloc(size);
	for(int i=0; i<100; i++) {
		*buffer = (char*)malloc(size);
		*buffer_calloc = (char*)calloc(size, sizeof(buffer));
		addrs[i] = *buffer_calloc;
	}
	return addrs;
}


void assign(char **buffer, char **buffer_calloc) {
	char *buf = *buffer_calloc ;
	allocate(buffer,&buf);
	int i =0;
	for(;;) {
		if((buf)[i]==NULL) printf("test "); //do stuff;
		else break;
		i++;
	}
	buf[0] = 100; //segfault here : fixed

}

void setup_config(struct sockaddr_in *localaddr) {
	localaddr->sin_family = AF_INET;
	localaddr->sin_addr.s_addr = inet_addr(ADDR);
	localaddr->sin_port = htons(PORT);  // Any local port will do
}

void create() {
	struct sockaddr_in localaddr;
	struct hostent *hostp;
	
	char *buffer, *buffer_calloc;
	int *a;

	int sockfd = socket(AF_INET, SOCK_STREAM, 0);
	setup_config(&localaddr);
	if (sizeof(struct sockaddr *)==sizeof(&localaddr)) //printf("matched");
	if(bind(sockfd, (struct sockaddr *)&localaddr, sizeof(localaddr))<0) printf("bind failed!!");

	int len = sizeof(localaddr);

	//if(listen(sockfd, 5)!=0) printf("listen failed");
	int connfd = accept(sockfd, (struct sockaddr*)&sockfd, &len);
	if(connfd<0) printf("hell yeah : accept failed!!!!!");

	read(connfd, buffer, 1000);
	write(connfd, buffer, 1000);

	printf("\n%s ",buffer);
}
struct hostent *getSock_obj(struct sockaddr_in cli){ 
	struct in_addr addr;
	inet_aton("1.1.1.1", &addr);
	return gethostbyaddr((const char*)&addr, sizeof(addr), cli.sin_family);
}

int main() {

	// Bind to a specific network interface (and optionally a specific local port)
	int i = 0;
	struct sockaddr_in localaddr;
	struct hostent *hostp;

	char *buffer, *buffer_calloc;
	int *a;
	
	assign(&buffer,&buffer_calloc);
	
	//buffer_calloc[10] = 100;
	
	//while(addr[i]!=NULL) {
		i++;
	//}

	//char *test = addr[0];
	
	//buffer_calloc[100] = 100;

	//for(int i=0; i<100; i++) (&buffer_calloc)[i] = 100;


	return 0;
}

