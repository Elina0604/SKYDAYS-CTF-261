#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

void ignore_me_init() {
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
}

char neutral[] = 
" /\\_/\\\n"
"( . . )\n"
" = w =\n";
char sad[] = 
" /\\_/\\\n"
"( -.- )\n"
" > ^ <\n";
char happy[] = 
" /\\___/\\\n"
"( =^.^= )\n"
"(\")__(\")\n";
char surprised[] = 
" /\\_/\\\n"
"( o.o )\n"
" > ^ <\n";


int make_choice(void);
void process_user_action(int choice, int *happiness);
int get_cat_state(int happiness);

void update_happiness_for_feeding(int *happiness);
void update_happiness_for_playing(int *happiness);
void update_happiness_for_insulting(int *happiness);

void display_feeding_result(void);
void display_playing_result(void);
void display_secret_info(void);
void display_invalid_choice(void);

void display_insulting_result(void);
void win(void);


int main() {
    ignore_me_init();
    int happiness = 100;

    printf("%s\n", neutral);
    printf("meow...\n");

    while (1) {
        int choice = make_choice();

        if (choice == -1) {
            continue;
        }

        process_user_action(choice, &happiness);
        
        int state = get_cat_state(happiness);

        if (state == -1) {
            printf("%s\n", sad);
            printf("Kedi mutsuzluktan öldü.\n");
            break;
        }
    }
    return 0;
}

int get_cat_state(int happiness) {
    if (happiness > 65) { // 66-100
        return 1;
    }
    if (happiness > 30) { // 31-65
        return 0;
    }
    // 0-30
    return -1;
}

int make_choice() {
    int choice;
    printf("\n1. Besle\n");
    printf("2. Oyun oyna\n");
    printf("3. Hakaret et\n");
    printf("4. Gizli bir sey ogren\n");
    printf("Seçiminizi girin (1-4)\n");
    printf("> ");
    fflush(stdout);

    if (scanf("%d", &choice) != 1) {
        int c;
        while ((c = getchar()) != '\n' && c != EOF);
        printf("Geçersiz seçim, lütfen bir sayı girin.\n");
        return -1;
    }

    int c;
    while ((c = getchar()) != '\n' && c != EOF);

    return choice;
}

void process_user_action(int choice, int *happiness) {
    switch (choice) {
        case 1:
            update_happiness_for_feeding(happiness);
            display_feeding_result();
            break;
        case 2:
            update_happiness_for_playing(happiness);
            display_playing_result();
            break;
        case 3:
            update_happiness_for_insulting(happiness);
            display_insulting_result();
            break;
        case 4:
            display_secret_info();
            break;
        default:
            display_invalid_choice();
            break;
    }
}


void update_happiness_for_feeding(int *happiness) {
    if (*happiness <= 90) {
        *happiness += 10;
    } else {
        *happiness = 100;
    }
}

void update_happiness_for_playing(int *happiness) {
    if (*happiness <= 80) {
        *happiness += 20;
    } else {
        *happiness = 100;
    }
}

void update_happiness_for_insulting(int *happiness) {
    if (*happiness >= 30) {
        *happiness -= 30;
    } else {
        *happiness = 0;
    }
}


void display_feeding_result(void) {
    char buffer[64];
    printf("Kediyi Besle > ");
    fflush(stdout);
    read(0, buffer, 63);
    printf("Kediye sunu verdin:\n ");
    printf(buffer);
    printf("%s\n", happy);
    printf("-oh ustam sifa\n");
}

void display_playing_result(void) {
    printf("%s\n", happy);
    printf("-aleley aleley\n");
}

void display_secret_info(void) {
    printf("Bu kadar kolay degil!\n");
}

void display_invalid_choice(void) {
    printf("Geçersiz seçim, lütfen 1-4 arasında bir değer girin.\n");
}


void display_insulting_result() {
    char buffer[32];
    printf("> ");
    fflush(stdout);
    fgets(buffer, 100, stdin);
    printf("%s\n", sad);
    printf("-yuh ayip oluyo\n");
    return;
}

void win() {
    system("/bin/sh");
    return;
}
