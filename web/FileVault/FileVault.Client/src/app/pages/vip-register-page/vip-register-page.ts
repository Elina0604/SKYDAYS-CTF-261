import { HttpErrorResponse } from '@angular/common/http';
import { Component } from '@angular/core';
import { AbstractControl, FormBuilder, FormGroup, ReactiveFormsModule, ValidationErrors, Validators } from '@angular/forms';
import { catchError, tap, throwError } from 'rxjs';
import { AuthService } from '../../services/auth.service';
import { Router, RouterLink } from '@angular/router';

@Component({
  selector: 'app-vip-register-page',
  imports: [ReactiveFormsModule, RouterLink],
  templateUrl: './vip-register-page.html',
  styleUrl: './vip-register-page.css',
})
export class VipRegisterPage {
  vipRegisterForm: FormGroup;

  constructor(private fb: FormBuilder, private authService: AuthService, private router: Router){
    this.vipRegisterForm = this.fb.group({
      userName: ['', [Validators.required, Validators.minLength(6), Validators.pattern('^[a-z0-9_]+$')]],
      password: ['', [Validators.required, Validators.minLength(6)]],
      confirmPassword: ['', [Validators.required, , Validators.minLength(6)]],
    }, { 
      validators: this.passwordMatchValidator 
    });   
  }

  onSubmit(){
    if(this.vipRegisterForm.valid){
      this.authService.vipRegister({userName: this.vipRegisterForm.value.userName, password: this.vipRegisterForm.value.password})
        .pipe(
          tap(() => {
            this.router.navigate(['/login']);
          }),
          catchError((err: HttpErrorResponse) => {
            const message = err.error ?? 'Beklenmeyen bir hata oluştu';
            window.alert(message);
            return throwError(() => err);
          })
        )
        .subscribe();
    }
  }

  passwordMatchValidator(control: AbstractControl): ValidationErrors | null {
    const password = control.get('password');
    const confirmPassword = control.get('confirmPassword');

    if (password && confirmPassword && password.value !== confirmPassword.value) {
      confirmPassword.setErrors({ passwordMismatch: true });
      return { passwordMismatch: true };
    }
    return null;
  }
}
