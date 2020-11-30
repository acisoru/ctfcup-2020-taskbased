#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <stdbool.h>

#define BUF_SIZE 256
#define MAX_USERNAME_SZ 256
#define MAX_PASS_SZ 256
#define MAX_USERS 16

#define ADMIN     1<<2
#define MODERATOR  1<<1
#define LISTENER  1<<0

#define isAdmin(x) x&ADMIN ? 1 : 0
#define isModerator(x) x&MODERATOR ? 1 : 0
#define isListener(x) x&LISTENER ? 1 : 0

#define SWAP_BITS(x, a, b) x & (255^ (((((x>>a)&1)^1)<<b) | ((((x>>b)&1)^1)<<a)) ) | (((x>>a)&1)<<b)|(((x>>b)&1)<<a)

static bool validate_invite(char* invite_code);
static unsigned char check_user(char* name, char* pass);
static void create_user(char* name, char* pass, unsigned char flags);
static bool delete_user(unsigned char user_id);
static bool auth();
static void register_user();
static bool login();
static void all_chats();
static void join_chat();
static void admin_panel();
static void create_chat(unsigned char* chatname);
static void delete_chat(unsigned char* chatname);

static char ave_msg[] = "                                     ___   ___\n"
                      " ___ _______ _  ___ ___ ___ _  _  __/ _ \\ <  /\n"
                      "/ _ `/ __/  ' \\/ -_|_-</ _ `/ | |/ / // / / / \n"
                      "\\_,_/_/ /_/_/_/\\__/___/\\_, /  |___/\\___(_)_/  \n"
                      "                      /___/                   \n"
					  "this is first version of console client armseg\n"
					  "Greetings from the 90s. Hope you enjoy!";
					  
static char register_banner[] = "                _     _            \n"
							  " _ __ ___  __ _(_)___| |_ ___ _ __ \n"
							  "| '__/ _ \\/ _` | / __| __/ _ \\ '__|\n"
							  "| | |  __/ (_| | \\__ \\ ||  __/ |   \n"
							  "|_|  \\___|\\__, |_|___/\\__\\___|_|   \n"
							  "          |___/                    ";

static char login_banner[]=" _             _       \n"
						"| | ___   __ _(_)_ __  \n"
						"| |/ _ \\ / _` | | '_ \\ \n"
						"| | (_) | (_| | | | | |\n"
						"|_|\\___/ \\__, |_|_| |_|\n"
						"         |___/         ";
		 
static char auth_menu[] = "1. Login\n2. Register\n3. Quit\n\nyour choise: ";

static char gamma[] = "\x9a\x9a\x95\xb3\x7a\x8f\xe2\xf2\xf3\xa4\x3a\x6d\xaa"
"\xe2\x30\x16\x98\xf5\x41\x17\x1a\x13\x03\x4e\xf2\xe2\xc4\x15\xa0\x40\xcf"
"\x8b\x9b\x39\x9b\x00\x45\x1e\x3c\x75\x8e\xa0\x73\x4d\x60\x67\xe9\x1b\x75"
"\x79\x83\xf9\x43\x27\x70\x34\x41\xfa\x5a\xf2\x70\xba\xd3\xf1\x2b\x05\x35"
"\x02\xf3\x4d\xdd\xde\x6d\x4c\xf0\xc8\x4e\xd5\xd3\x32\x73\x11\x43\x89\x2b"
"\xf8\x0b\x70\xc2\xa4\x90\x57\xfb\xa7\x5d\xf8\x35\x95\x0a\xd6\x03\x03\x9c"
"\xad\xeb\xb5\x84\x43\xeb\xf5\x0f\x19\xfb\xe7\x59\xcf\xdc\x87\x1c\x46\x9e"
"\x29\x63\x3a\xbc\x32\x3e\xd9\x7e\xfc\xb8\x0c\xa6\x1e\xc3\xfd\x15\x29\x5b"
"\x9f\xa2\xa8\xf0\xff\x7d\xb4\xb9\x93\x98\xce\x0b\xf8\xe1\x0a\x5b\x7c\x27"
"\x6b\x25\xc2\x1a\xc6\x18\x9b\x04\xf8\x64\x8f\x95\x41\xe8\xaa\x68\x88\xa8"
"\xd5\xed\x3c\xe4\x22\xd0\x8a\xf1\x1b\x8f\x12\xd7\x20\x5a\xd4\x2e\xbc\xdf"
"\x9b\xe2\x97\xeb\xb7\x76\xdc\x19\x7f\x24\x6a\x3e\x55\x9c\xfe\x09\x4f\x27"
"\xbc\x5a\xb0\x45\x46\xa6\xa0\xd1\x3a\x99\xe3\x1c\x2b\x3c\xc2\xe2\xef\x15"
"\x3c\xfa\x23\x53\x77\xb7\x6c\x6c\x6f\xfa\x90\xcd\x1f\xb5\x37\xc1\x6b\x67"
"\xd5\xcd\x6f\xc7\xa8\xd3\xc4\xdd\x14";

static char secret_code[] = "\xbe\x68\x29\x74\xb2\xbd\xb4\x35\x13\x71\x45"
"\x55\x56\x47\xe3\x9b\xef\x25\x1d\x9b\x4b\xdf\x58\xdd\x61\x31\x39\x49\x24"
"\x5a\x2d\xb9\xbd\x55\xfb\x5c\x49\xde\x01\x84\x42\x6b\x08\xd0\x0a\x4d\xbb"
"\x27\xdf\x1f\xd6\xbe\x36\x1d\x8b\xdb\x04\xf9\x33\x3d\x8b\xa9\x53\x3a\xc9"
"\x54\x8f\x32\x29\xd0\xf4\x83\x8a\xc4\x2e\xf5\xf6\x70\x53\x5c\x08\xc5\x36"
"\xb1\xc9\xea\xa2\x8b\xc2\x7b\x24\xa7\xad\xbc\x55\xea\x8f\x20\xb6\x57\x76"
"\x76\xf0\xeb\x2c\x6a\x31\x36\x2c\x2a\xb2\x15\xad\xec\x45\x46\xb0\xc6\x51"
"\x72\xc3\xda\x5d\x88\xaa\x5c\x98\xe4\xc8\xfa\xba\x94\xe8\x63\x96\xae\xd5"
"\xda\x77\x97\xf8\xef\x2e\xbd\x0f\x7e\xfe\x03\xe0\x02\xa2\xea\x6f\xb6\x77"
"\x5b\x1d\x89\x0e\xc2\x73\xd2\x41\x87\x10\xea\x1a\x16\x20\x04\xaf\x28\x8e"
"\xa5\xef\x70\xab\x0b\x3b\x59\x74\x52\x3a\x27\x16\xb3\x43\x4a\x33\x64\xcd"
"\xaa\xc7\x87\xb8\x13\x2c\x79\x0c\xb0\x15\x9c\x5a\x9d\x98\x95\xf0\xe9\x90"
"\xe2\x1d\xaa\x33\x6e\x14\x72\xe8\x6b\x60\x88\xb4\xfc\x51\xc9\x0b\xc2\xb8"
"\x3c\xd5\x0b\xf9\x0d\xb7\x18\x79\x9e\x9e\x99\xf9\x24\xf1\x37\x6a\x58\x25"
"\x89\x4d\x70\xf1\x99\x86\xef\x53\x61\xf4\x91";

struct user{
	char username[MAX_USERNAME_SZ];
	char password[MAX_PASS_SZ];
	unsigned char flags;
};

struct chat{
	struct chat* prev_chat;
	struct chat* next_chat;
	char chatname[BUF_SIZE];
	char* messages[BUF_SIZE];
};

static struct user users[MAX_USERS];

struct chat* chat_list = NULL;

static unsigned char users_count = 0;

static unsigned char current_user;

static void hello_msg(){
	printf("%s\n",ave_msg);
}

static bool validate_invite(char* invite_code){
	for(unsigned int i=0; i<BUF_SIZE; i++){
		invite_code[i] ^= gamma[i];
		invite_code[i] = SWAP_BITS(invite_code[i],3,4);
		invite_code[i] = SWAP_BITS(invite_code[i],2,7);
		invite_code[i] = SWAP_BITS(invite_code[i],0,5);
		invite_code[i]*=67;
		invite_code[i] = SWAP_BITS(invite_code[i],5,2);
		invite_code[i] = SWAP_BITS(invite_code[i],3,0);
		invite_code[i] = SWAP_BITS(invite_code[i],7,4);
 	}
	return !memcmp(secret_code, invite_code, BUF_SIZE);
}

static unsigned char check_user(char* name, char* pass){
	for(unsigned char i=0; i < users_count; i++){
		if(!memcmp(&users[i].username, name, BUF_SIZE)&&
		!memcmp(&users[i].password, pass, BUF_SIZE))
			return i;
	}
	return 0xff;
}

static void create_user(char* name, char* pass, unsigned char flags){
	memcpy(&users[users_count].username, name, MAX_USERNAME_SZ);
	memcpy(&users[users_count].password, pass, MAX_PASS_SZ);
	users[users_count].flags = flags;
	users_count++;
}

static bool delete_user(unsigned char user_id){
	for(unsigned char i=user_id; i < (users_count-1); i++){
		memcpy(&users[i].username, &users[i+1].username, BUF_SIZE);
		memcpy(&users[i].password, &users[i+1].password, BUF_SIZE);
		users[i].flags = users[i+1].flags;
	}
	users_count--;
}

static bool auth(){
	for(unsigned char try=0; try<3; ){
		unsigned char option;
		printf("%s",auth_menu);
		scanf(" %c",&option);
		option -= 48;
		switch(option)
		{
		case 1:
			if(login())
				return true;
			else
				try++;
			printf("%s\n","Incorrect login or password");
			break;
		case 2:
			register_user();
			break;
		case 3:
			try += 3;
			break;
		}
	}
	return false;
}

static void register_user(){
	char option;
	char invite_code[BUF_SIZE];
	char username[MAX_USERNAME_SZ];
	char password[MAX_PASS_SZ];
	printf("%s\n",register_banner);
	printf("%s","For Register in our system you need to have invite code. \nDo you have?[y/n] ");
	scanf(" %c",&option);
	if(option != 'y'){
		printf("%s\n","Sry, need to have invite code");
		return;
	}
	memset(invite_code, 0, BUF_SIZE);
	printf("%s","Enter invite code: ");
	scanf(" %255s", invite_code);
	if(!validate_invite(invite_code)){
		printf("%s\n","invalid invite code");
		return;
	}
	printf("%s","You are welcome!\n");
	if(users_count >= MAX_USERS){
		printf("%s\n","Sry, too many users registered");
	}
	memset(username, 0, MAX_USERNAME_SZ);
	memset(password, 0, MAX_PASS_SZ);
	printf("%s","Enter username: ");
	scanf(" %255s",username);
	printf("%s","Enter password: ");
	scanf(" %255s",password);
	create_user(username, password, LISTENER);
	printf("%s %s\n","Success, created new user", username);
}

static bool login(){
	char username[MAX_USERNAME_SZ];
	char password[MAX_PASS_SZ];
	memset(username, 0, MAX_USERNAME_SZ);
	memset(password, 0, MAX_PASS_SZ);
	printf("%s\n",login_banner);
	printf("%s","Enter username: ");
	scanf(" %255s",username);
	printf("%s","Enter password: ");
	scanf(" %255s",password);
	current_user = check_user(username, password);
	if(current_user!=0xff)
		return true;
	return false;
}

static void main_service(){
	for(bool stop = false; stop!=true;){
		unsigned char option;
		printf("%s %s\n", "Welcome", users[current_user].username);
		if(isListener(users[current_user].flags)||isModerator(users[current_user].flags))
			printf("%s","Menu: \n 1. Chats List\n 2. Join in chat\n 0. Quit\n$ ");
		if(isAdmin(users[current_user].flags))
			printf("%s","Menu: \n 1. Chats List\n 2. Join in chat\n 3. Admin panel\n 0. Quit\n$ ");
		scanf(" %c",&option);
		option -= 48;
		switch(option)
		{
		case 0:
			stop = true;
			break;
		case 1:
			all_chats();
			break;
		case 2:
			join_chat();
			break;
		case 3:
			admin_panel();
		}
	}
}

static void all_chats(){
	struct chat* current_chat = chat_list;
	if(chat_list==NULL){
		printf("%s\n","no enough chats :)");
		return;
	}
	do{
		printf(current_chat->chatname);
		putchar('\n');
		current_chat = current_chat->next_chat;
	}
	while(current_chat != chat_list);
}

static void join_chat(){
	char chatname[BUF_SIZE];
	memset(chatname, 0, MAX_USERNAME_SZ);
	if(chat_list==NULL){
		printf("%s\n","no enough chats :)");
		return;
	}
	printf("%s","Enter chatname: ");
	scanf(" %255s",chatname);
	struct chat* current_chat = chat_list;
	do{
		if(!strcmp(current_chat->chatname,chatname))
			break;
		current_chat = current_chat->next_chat;
	}
	while(current_chat != chat_list);
	if(strcmp(current_chat->chatname,chatname)){
		printf("%s","chat not found");
		return;
	}
	printf("%s\n","Enter ++leave to leave from chat");
	for(unsigned int i=0; i<BUF_SIZE; i++){
		if(current_chat->messages[i]){
			printf("%s\n",current_chat->messages[i]);
		}
		else{
			current_chat->messages[i] = malloc(BUF_SIZE);
			scanf(" %255s",current_chat->messages[i]);
			if(!strcmp(current_chat->messages[i],"++leave"))
				return;
		}
	}
}

static void admin_panel(){
	for(bool stop = false; stop!=true;){
		unsigned char option;
		char username[MAX_USERNAME_SZ];
		char password[MAX_PASS_SZ];
		char chatname[BUF_SIZE];
		char flags;
		unsigned char id;
		memset(chatname, 0, BUF_SIZE);
		memset(username, 0, MAX_USERNAME_SZ);
		memset(password, 0, MAX_PASS_SZ);
		printf("%s %s\n", "Welcome", users[current_user].username);
		printf("%s","Menu: \n 1. Create chat\n 2. Delete chat\n 3. Create user\n 4. Delete user\n 0. Back\n# ");
		scanf(" %c",&option);
		option -= 48;
		switch(option)
		{
		case 0:
			stop = true;
			break;
		case 1:
			printf("%s","Enter chatname: ");
			scanf(" %255s",chatname);
			create_chat(chatname);
			break;
		case 2:
			printf("%s","Enter chatname: ");
			scanf(" %255s",chatname);
			delete_chat(chatname);
			break;
		case 3:
			printf("%s","Enter username: ");
			scanf(" %255s",username);
			printf("%s","Enter password: ");
			scanf(" %255s",password);
			printf("%s","Is admin?[y/n]");
			scanf(" %c",&flags);
			if(flags=='y')
				create_user(username,password, ADMIN);
			else
				create_user(username, password, LISTENER);
			break;
		case 4:
			printf("%s","Enter userid: ");
			scanf(" %c",&id);
			delete_user(id);
			break;
		}
	}
}

static void create_chat(unsigned char* chatname){
	struct chat* new_chat = NULL;
	if(chat_list==NULL){
		chat_list = malloc(sizeof(struct chat));
		chat_list->prev_chat = chat_list;
		chat_list->next_chat = chat_list;
		memcpy(chat_list->chatname, chatname, BUF_SIZE);
		return;
	}
	new_chat = malloc(sizeof(struct chat));
	new_chat->next_chat = chat_list;
	chat_list->prev_chat->next_chat = new_chat;
	new_chat->prev_chat = chat_list->prev_chat;
	chat_list->prev_chat = new_chat;
	memcpy(new_chat->chatname, chatname, BUF_SIZE);
}

static void delete_chat(unsigned char* chatname){
	struct chat* del_chat = chat_list;
	if(chat_list==NULL){
		return;
	}
	do{
		if(!strcmp(del_chat->chatname,chatname))
			break;
		del_chat = del_chat->next_chat;
	}
	while(del_chat != chat_list);
	if(strcmp(del_chat->chatname,chatname))
		return;
	del_chat->prev_chat->next_chat = del_chat->next_chat;
	del_chat->next_chat->prev_chat = del_chat->prev_chat;
	for(unsigned int i=0; i<BUF_SIZE; i++){
		if(del_chat->messages[i])
			free(del_chat->messages[i]);
	}
	if(chat_list->prev_chat == chat_list){
		free(chat_list);
		chat_list = NULL;
		return;
	}
	if(del_chat == chat_list)
		chat_list = del_chat->next_chat;
	free(del_chat);
	del_chat = NULL;
}

int main(){
	setvbuf(stdout, 0, 2, 0);
  	setvbuf(stderr, 0, 2, 0);
  	setvbuf(stdin, 0, 2, 0);
	hello_msg();
	if(auth()){
		main_service();
		printf("%s\n","Success");
	}
	printf("%s\n","Goodbuy!");
	system("exit");
	return 0;
}