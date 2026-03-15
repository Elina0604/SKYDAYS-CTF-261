#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

#ifdef CATFILE
void cat_file(const char* fname) {
    FILE *file;
    char ch;

    file = fopen(fname, "r");
    if (file == NULL) {
        perror("cat_file");
        exit(-1);
    }

    while ((ch = fgetc(file)) != EOF) {
        putchar(ch);
    }

    fclose(file);
}
#endif

void menu() {
    puts("1) Read memory");
    puts("2) Write memory");
    puts("3) Exit");
}

void read_mem() {
    void *addr;
    size_t size;
    char buf[128];

    puts("Format: <addr:%p> <size:decimal>");
    printf("addr size: ");

    fgets(buf, sizeof(buf), stdin);
    sscanf(buf, "%p %zu", &addr, &size);

    write(1, addr, size);   // raw memory output
}

void write_mem() {
    void *addr;
    size_t size;
    char buf[128];

    puts("Format: <addr:%p> <size:decimal>");
    printf("addr size: ");

    fgets(buf, sizeof(buf), stdin);
    sscanf(buf, "%p %zu", &addr, &size);

    printf("Input %zu bytes:\n", size);

    read(0, addr, size);
}

int main() {
    char buf[32];
    int choice;
    int run = 1;

    setbuf(stdout, NULL);
    setbuf(stdin, NULL);

#ifdef CATFILE
    printf("ASLR sorun degil\n");
    cat_file("/proc/self/maps");

    void **ret_addr_ptr;
    ret_addr_ptr = (void **)(__builtin_frame_address(0) + sizeof(void *));
    printf("Return address: %p\n", ret_addr_ptr);
#else
    printf("main burada, gerisi sende: %p\n", &main);
#endif

    while(run) {
        menu();

        printf("> ");
        fgets(buf, sizeof(buf), stdin);
        choice = atoi(buf);

        switch(choice) {
            case 1:
                read_mem();
                break;
            case 2:
                write_mem();
                break;
            case 3:
                puts("Bye");
                // exit(0);
                run = 0;
                break;
            default:
                puts("Invalid");
        }
    }

    return 0;
}
