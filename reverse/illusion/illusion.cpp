#include <iostream>
#include <string>

unsigned char flag_arr[] =
{
    0x42, 0x53, 0x1B, 0x24, 0x76, 0x69, 0x56, 0x21, 0x71, 0x26,
    0x3C, 0x20, 0x4C, 0x04, 0x6F, 0x76, 0x2D, 0x2F, 0x61, 0x85
};

class base 
{
public:
    virtual unsigned char m1(unsigned char c) = 0;
    virtual unsigned char m2(unsigned char c) = 0;
    virtual unsigned char m3(unsigned char c) = 0;
};

class d1: public base 
{
public:
    unsigned char m1(unsigned char c) override { return c ^ 0x42; }
    unsigned char m2(unsigned char c) override { return c + 0x10; }
    unsigned char m3(unsigned char c) override { return c - 0x05; }
};

class d2 : public base 
{
public:
    unsigned char m1(unsigned char c) override { return c + 0x08; }
    unsigned char m2(unsigned char c) override { return c ^ 0x37; }
    unsigned char m3(unsigned char c) override { return c ^ 0x5A; }
};

class d3 : public base 
{
public:
    unsigned char m1(unsigned char c) override { return c ^ 0x11; }
    unsigned char m2(unsigned char c) override { return c - 0x20; }
    unsigned char m3(unsigned char c) override { return c + 0x03; }
};

void swap(void* a, void* b) 
{
    void** vptr_a = *(void***)a;
    void** vptr_b = *(void***)b;
    *(void***)a = vptr_b;
    *(void***)b = vptr_a;
}

typedef unsigned char(*vfunc)(void*, unsigned char);

unsigned char invoke(void* obj, int m_idx, unsigned char c) 
{
    void** vtable = *(void***)obj;
    vfunc f = (vfunc)vtable[m_idx];
    return f(obj, c);
}


int main() 
{
    std::string input;
    std::cout << "Enter flag: ";
    std::cin >> input;

    if (input.length() != 20) 
    {
        std::cout << "Invalid flag\n";
        return 1;
    }

    d1* i1 = new d1();
    d2* i2 = new d2();
    d3* i3 = new d3();
    
    swap(i1, i3);

    void* instances[] = { i1, i2, i3 };
  
    for (int i = 0; i < 20; ++i) 
    {
        int eng_idx = i % 3;
        int meth_idx = (i / 3) % 3;

        unsigned char out = invoke(instances[eng_idx], meth_idx, input[i]);

        if (out != flag_arr[i]) 
        {
            std::cout << "Invalid flag.\n";
            return 1;
        }
    }

    std::cout << "Congrats!" << std::endl;
    std::cin.get();
    std::cin.get();
    
    return 0;
}
