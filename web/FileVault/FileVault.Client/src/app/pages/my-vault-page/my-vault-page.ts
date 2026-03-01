import { ChangeDetectorRef, Component, OnInit } from '@angular/core';
import { FileService } from '../../services/file.service';
import { catchError, tap, throwError } from 'rxjs';
import { HttpErrorResponse } from '@angular/common/http';

@Component({
  selector: 'app-my-vault-page',
  imports: [],
  templateUrl: './my-vault-page.html',
  styleUrl: './my-vault-page.css',
})
export class MyVaultPage implements OnInit{
  myFileNames: string[] = [];
  usedSpaceAsMB: number = 0;
  isModalOpen = false;
  selectedFile: File | null = null;
  allowedExtensions = ['pdf', 'png'];

  constructor(private fileService: FileService, private cdr: ChangeDetectorRef){}

  ngOnInit(): void {
    this.fileService.getMyFileNames()
      .pipe(
        tap((response) => {
          this.myFileNames = response;
          if(this.myFileNames.length != 0){
            this.fileService.getMyUsedSpaceAsMB()
              .pipe(
                tap((response) => {
                  this.usedSpaceAsMB = response;
                  this.cdr.detectChanges();
                }),
                catchError((err: HttpErrorResponse) => {
                  const message = err.error?.error?.message ?? 'Beklenmeyen bir hata oluştu';
                  window.alert(message);
                  return throwError(() => err);
                })
              )
              .subscribe();
          }
          else{
            this.usedSpaceAsMB = 0;
            this.cdr.detectChanges();
          }
        }),
        catchError((err: HttpErrorResponse) => {
          const message = err.error?.error?.message ?? 'Beklenmeyen bir hata oluştu';
          window.alert(message);
          return throwError(() => err);
        })
      )
      .subscribe();
  }

  openUploadModal() {
    this.isModalOpen = true;
  }

  closeUploadModal() {
    this.isModalOpen = false;
    this.selectedFile = null;
  }

  onFileSelected(event: any) {
    const input = event.target as HTMLInputElement;
    if (input.files && input.files.length > 0) {
      const file = input.files[0];
      const parts = file.name.split('.');
      if(parts.length != 2){
        window.alert('Dosya adı formatı file_name.extension olmalı');
        return;
      }

      if (this.allowedExtensions.includes(parts[1])) {
        this.selectedFile = file;
      } 
      else {
        window.alert('Yalnızca .pdf ve .png dosyalarına izin verilir!');
        input.value = '';
        this.selectedFile = null;
      }
    }
  }

  onUpload() {
    if (this.selectedFile != null) {
      const fileToUpload = this.selectedFile;
      this.closeUploadModal();
      this.fileService.uploadFile(fileToUpload).pipe(
      tap(() => {
        window.location.reload();
      }),
      catchError((err: HttpErrorResponse) => {
        const message = err.error.split('.')[0] ?? 'Beklenmeyen bir hata oluştu';
        window.alert(message);
        return throwError(() => err);
      })
    ).subscribe();
    }
  }

  onDownload(fileName: string) {
    this.fileService.download(fileName).pipe(
      tap(({ blob, fileName }) => {
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = fileName;
        a.click();
        window.URL.revokeObjectURL(url);
      }),
      catchError((err: HttpErrorResponse) => {
        const message = err.error?.error?.message ?? 'Beklenmeyen bir hata oluştu';
        window.alert(message);
        return throwError(() => err);
      })
    ).subscribe();
  }

  onDelete(fileName: string) {
    this.fileService.delete(fileName).pipe(
      tap(() => {
        window.location.reload();
      }),
      catchError((err: HttpErrorResponse) => {
        const message = err.error?.error?.message ?? 'Beklenmeyen bir hata oluştu';
        window.alert(message);
        return throwError(() => err);
      })
    ).subscribe();
  }
}
