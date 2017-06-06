/*
Compile command
gcc -shared -fPIC -m32 -o armaxpy.so armaxpy.c 
*/
#include<stdio.h>
#include<string.h>
#include<strings.h>
#include<sys/socket.h>
#include<arpa/inet.h>
#include <unistd.h>
#define IP "127.0.0.1"
#define PORT 8888
#define MAXSIZE 10240

const char* server(const char* stringa)
{
    int sock;
    struct sockaddr_in server;
    char server_reply[MAXSIZE];
    const char* p_sr;
    p_sr = server_reply;

    //Create socket
    sock = socket(AF_INET, SOCK_STREAM, 0);

    server.sin_addr.s_addr = inet_addr(IP);
    server.sin_family = AF_INET;
    server.sin_port = htons(PORT);

    //Connect to server
    if (connect(sock, (struct sockaddr*)&server, sizeof(server)) < 0) {
        return stringa;
    }
    char safestringa[512];
    strcpy(safestringa, stringa);
    //Send data
    if (send(sock, safestringa, strlen(safestringa), 0) < 0) {
        return stringa;
    }
    //Receive reply
    if (recv(sock, server_reply, MAXSIZE, 0) < 0) {
        
    }

    close(sock);
    return p_sr;
}

int parameterSafeCheck(char* string)
{
    int i;
    for (i = 0; i < (strlen(string) - 1); i++) {
        char curChar = string[i];
        if (curChar == '&') {
            return 1;
        }
    }
    return 0;
}

int isServerStarted(char *_address,int _port)
{
    struct sockaddr_in server;
    int sock = socket(AF_INET, SOCK_STREAM, 0);
    server.sin_addr.s_addr = inet_addr(_address);
    server.sin_family = AF_INET;
    server.sin_port = htons(_port);
    int isbinded = bind(sock, (struct sockaddr *) &server, sizeof(server)) < 0;
    return isbinded;
}

void RVExtension(char* output, int outputSize,const char* function)
{
/*    int isBinded = isServerStarted(IP,PORT);
    if (!isBinded) {
        system("python3 ./@armaxpy/armaxpy_server.pyc &");
    } */
    int condition = parameterSafeCheck(function);
    if (condition) {
        strncpy(output, server(function), outputSize);
    }
    else {
        strncpy(output, function, outputSize);
    }
output[outputSize - 1] = '\0';
return;
}
