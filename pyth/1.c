#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <math.h>
    //                 c = 2 (50)   0(48)    9(57)
int char_to_digit(char c) {
    if (c >= '0' && c <= '9') {
        return c - '0';
    } else if (c >= 'A' && c <= 'F') {
        return c - 'A' + 10;   //A(65)
    }
    return -1;
}

char digit_to_char(int digit) {
    if (digit >= 0 && digit <= 9) {
        return '0' + digit;
    } else if (digit >= 10 && digit <= 15) {
        return 'a' + (digit - 10);
    }
    return '?';
}

int is_valid_number(const char* num_str, int base) {
    int len = strlen(num_str);
    if (len == 0 || len > 13) {
        return 0;
    }
    
    int dot_count = 0;
    for (int i = 0; i < len; i++) {
        if (num_str[i] == '.') {    
            dot_count++;            
            // Проверка на точку в начале или конце
            if (i == 0 || i == len - 1) {
                return 0;
            }
        } else {
            int digit = char_to_digit(num_str[i]);
            if (digit == -1 || digit >= base) {
                return 0;
            }
        }
    }
    
    if (dot_count > 1) {
        return 0;
    }
    
    return 1;
}

int main() {
    int b1, b2;
    char num_str[14];
    
    // Чтение входных данных
    if (scanf("%d %d", &b1, &b2) != 2) {
        printf("bad input\n");
        return 0;
    }
    
    if (scanf("%13s", num_str) != 1) {
        printf("bad input\n");
        return 0;
    }
    
    // Проверка оснований систем счисления
    if (b1 < 2 || b1 > 16 || b2 < 2 || b2 > 16) {
        printf("bad input\n");
        return 0;
    }
    
    // Проверка корректности числа
    if (!is_valid_number(num_str, b1)) {
        printf("bad input\n");
        return 0;
    }
    
    // Разделение на целую и дробную части
    char integer_part[14] = "0"; 
    char fractional_part[14] = "0";
    int has_fractional = 0;
    
    char* dot_ptr = strchr(num_str, '.'); 
    if (dot_ptr != NULL) {
        has_fractional = 1;
        // Копируем целую часть     1234567.1234235
        int int_len = dot_ptr - num_str;
        if (int_len > 0) {
            strncpy(integer_part, num_str, int_len);
            integer_part[int_len] = '\0';
        }
        // Копируем дробную часть
        strcpy(fractional_part, dot_ptr + 1);
    } else {
        strcpy(integer_part, num_str);
    }
    
    // Перевод целой части в десятичную систему
    long long integer_decimal = 0;
    for (int i = 0; integer_part[i] != '\0'; i++) {
        integer_decimal = integer_decimal * b1 + char_to_digit(integer_part[i]);
    }
    
    // Перевод дробной части в десятичную систему
    double fractional_decimal = 0.0;
    double power = 1.0 / b1;
    for (int i = 0; fractional_part[i] != '\0'; i++) {
        fractional_decimal += char_to_digit(fractional_part[i]) * power;
        power /= b1;
    }
    
    // Перевод целой части в систему счисления b2
    char integer_result[50] = "0";
    if (integer_decimal == 0) {
        integer_result[0] = '0';
        integer_result[1] = '\0';
    } else {
        long long n = integer_decimal;
        int idx = 0;
        char temp[50];
        
        while (n > 0) {
            int digit_value = n % b2;
            temp[idx++] = digit_to_char(digit_value);
            n /= b2;
        }
        
        // Разворачиваем результат
        for (int i = 0; i < idx; i++) {
            integer_result[i] = temp[idx - 1 - i];
        }
        integer_result[idx] = '\0';
    }
    
    // Перевод дробной части в систему счисления b2 (12 знаков)
    char fractional_result[13];
    double fractional = fractional_decimal;
    
    for (int i = 0; i < 12; i++) {
        fractional *= b2;
        int digit = (int)fractional;
        fractional_result[i] = digit_to_char(digit);
        fractional -= digit;
    }
    fractional_result[12] = '\0';
    
    // Вывод результата
    if (!has_fractional || strcmp(fractional_part, "0") == 0) {
        printf("%s\n", integer_result);
    } else {
        printf("%s.%s\n", integer_result, fractional_result);
    }
    
    return 0;
}