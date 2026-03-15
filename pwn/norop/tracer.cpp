#include <iostream>
#include <sys/ptrace.h>
#include <sys/user.h>
#include <sys/wait.h>
#include <unistd.h>
#include <stack>
#include <capstone/capstone.h>

void run_tracer(pid_t child_pid) {
    int status;
    std::stack<unsigned long long> shadow_stack;
    struct user_regs_struct regs;
    csh handle;

    // Initialize Capstone for x86_64
    if (cs_open(CS_ARCH_X86, CS_MODE_64, &handle) != CS_ERR_OK) return;

    while (true) {
        waitpid(child_pid, &status, 0);
        if (WIFEXITED(status)) break;

        ptrace(PTRACE_GETREGS, child_pid, NULL, &regs);

        // Read 16 bytes from the current RIP to decode the instruction
        unsigned char code[16];
        for (int i = 0; i < 2; i++) {
            long data = ptrace(PTRACE_PEEKTEXT, child_pid, regs.rip + (i * 8), NULL);
            reinterpret_cast<long*>(code)[i] = data;
        }

        cs_insn *insn;
        size_t count = cs_disasm(handle, code, sizeof(code), regs.rip, 1, &insn);

        if (count > 0) {
            std::string mnemonic = insn[0].mnemonic;

            // --- Handle ALL types of CALLs ---
            if (mnemonic == "call") {
                // The return address is RIP + length of the current instruction
                shadow_stack.push(regs.rip + insn[0].size);
            } 
            // --- Handle ALL types of RETs ---
            else if (mnemonic == "ret") {
                if (!shadow_stack.empty()) {
                    unsigned long long real_ret = ptrace(PTRACE_PEEKDATA, child_pid, regs.rsp, NULL);
                    unsigned long long expected = shadow_stack.top();
                    shadow_stack.pop();

                    if (real_ret != expected) {
                        std::cout << "\n[!] ATTACK DETECTED AT 0x" << std::hex << regs.rip << std::endl;
                        std::cout << "[!] Shadow Stack expected 0x" << expected << " but found 0x" << real_ret << std::endl;
                        ptrace(PTRACE_KILL, child_pid, NULL, NULL);
                        break;
                    }
                }
            }
            cs_free(insn, count);
        }

        ptrace(PTRACE_SINGLESTEP, child_pid, NULL, NULL);
    }
    cs_close(&handle);
}

int main(int argc, char** argv) {
    if (argc < 2) {
        std::cerr << "Usage: " << argv[0] << " <binary_path>" << std::endl;
        return 1;
    }

    pid_t pid = fork();
    if (pid == 0) {
        // Child Process
        ptrace(PTRACE_TRACEME, 0, NULL, NULL);
        execl(argv[1], argv[1], NULL);
    } else {
        // Parent Process
        run_tracer(pid);
    }
    return 0;
}
