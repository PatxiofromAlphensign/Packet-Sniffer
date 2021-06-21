#include <stdio.h> 
#include <netdb.h>
#include <netinet/in.h>
#include<unistd.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <sys/types.h>
#define MAX 80
#define PORT 8081 // PORT being used for more than the indended purposes
#define SA struct sockaddr

// TODO document features and modes being used
// TODO make homogenous type struct for iterating server meta_data

struct server_status {
	char *test, *addr, *port, *fuck;
	char arr[4];
};

union iter_server_status {
	struct server_status sv;
	uint16_t arr[sizeof(struct server_status)];
};

char *genstr(char *data)  {	// overflow genarator
	char *_data = (char*)malloc(PORT);
	for(int i=0;i<10; i++) strcat(_data,data);
	return _data;
}

int* make_childs(){
	struct server_status *sv;
	//int x = (int)sv[0];
} 
void get(int sockfd){ // iteraction 
	char* buff =  (char*)malloc(sizeof(PORT));
	for (;;) {
		//recv(sockfd, buff, sizeof(buff), 0);
		read(sockfd, buff, sizeof(buff));
		printf("%s", buff);
		if(!buff) break;
		buff = genstr(buff);
		write(sockfd, buff, sizeof(buff));
		if(!strncmp("exit", buff, 4)) break ;
	}
}
void iter_server_struct(struct server_status *ss) {
	char *names[] = {"fuck","localhost","8080"};
	for(int idx=0; names[idx]!=NULL; idx++) {
		if(idx<sizeof(ss)) {
			((char**)ss)[idx] = names[idx];
		}
	} 
}
void iter_server_union(union  iter_server_status *i) {
	uint16_t *names[] = {(uint16_t*)"fuck",(uint16_t*)"localhost", (uint16_t*)"8080"};
	union  iter_server_status* iter = (union iter_server_status*)malloc(sizeof(union iter_server_status)); 
	memcpy(i, names, sizeof(i));

	for(int idx=0; i->arr[idx];i++) {
		i->arr[idx] = *names[idx]; //segFault on assignment
	}
}

void config_grpah() {
// config grpah: create arr relations & edges for the network config {overkil: i don't know }

	
	
}

int main() {

	struct sockaddr_in cli, serveraddr;
	int sockfd = socket(AF_INET, SOCK_STREAM, 0);
	//get(sockfd);
	//
	cli.sin_family = AF_INET;
	cli.sin_addr.s_addr = htons("1.1.1.1"); 
	cli.sin_port = htons(PORT);
	if ((int)cli.sin_addr.s_addr>0) {
		cli.sin_addr.s_addr=inet_addr("192.168.29.167");
		cli.sin_port =  8081;
	}

	/* printf("trying to bind to %d ", inet_addr("192.168.29.167")); */

/* 	if (bind(sockfd, (SA*)&cli, sizeof(cli)))  { */
/* 		printf("failed\n"); */
/* 		exit(0); */
/* 	} */

	/* if(listen(sockfd, 5)!=0) {printf("listen falied"); exit(0);} */

	int len = sizeof(serveraddr);
	int connfd =accept(sockfd, (SA*)&cli, &len);
	// break : setup_server_status
	union iter_server_status isv, isv_prime;
	struct server_status ss;
	//iter_server_union(&isv);
	iter_server_struct(&ss);
	printf("%s",(ss.addr));
	//get(connfd);
	return 0;
} 

