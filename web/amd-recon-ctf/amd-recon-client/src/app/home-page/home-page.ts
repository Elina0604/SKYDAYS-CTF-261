import { Component } from '@angular/core';
import { Question } from '../models/Question';
import { FormsModule } from '@angular/forms';
import { CommonModule, NgFor } from '@angular/common';

@Component({
  selector: 'app-home-page',
  imports: [FormsModule, NgFor, CommonModule],
  templateUrl: './home-page.html',
  styleUrl: './home-page.css',
})
export class HomePage {
  questions: (Question & { isCorrect?: boolean })[] = [
    new Question(1, 'What is the secret route?', '/******-*****', ''),
    new Question(2, 'What is the abbreviation that you got from the numbers in secret route?', '***', ''),
    new Question(3, 'What is the secret url?', 'https://hub.docker.com/r/*******/*******************/****', ''),
    new Question(4, 'What is the secret minecraft players name?', '*****', ''),
    new Question(5, 'This player has a Youtube channel, when was this channel started?', '******** *, ****', '')
  ];

  currentQuestionIndex: number = 0;
  flag: string | null = null;
  flagLoading = false;

  constructor() {
    this.loadAnswers();
  }

  downloadWordlist() {
    const link = document.createElement('a');
    link.href = 'custom_wordlist.txt';
    link.download = 'custom_wordlist.txt';
    link.click();
  }

  async checkAnswer(index: number, answer: string) {
    const question = this.questions[index];
    const userAnswer = answer.trim();

    if(!this.isFormatCorrect(userAnswer, question.placeHolder)){
      question.isCorrect = false;
    }
    else{
      const isCorrect = await this.verifyAnswerBackend(question.id, userAnswer);
      
      if (isCorrect) {
        question.answer = userAnswer; 
        question.isCorrect = true;
        if (this.currentQuestionIndex === index) {
          this.currentQuestionIndex++;
        }
      } else {
        question.isCorrect = false;
      }
    }

    this.saveAnswers();
  }

  saveAnswers() {
    const data = this.questions.map(q => ({
      id: q.id,
      answer: q.answer,
      isCorrect: q.isCorrect
    }));
    localStorage.setItem('questions', JSON.stringify(data));
  }

  loadAnswers() {
    const stored = localStorage.getItem('questions');
    if (!stored) return;

    try {
      const data = JSON.parse(stored) as { id: number, answer: string, isCorrect?: boolean }[];
      for (const q of data) {
        const question = this.questions.find(x => x.id === q.id);
        if (question) {
          question.answer = q.answer;
          question.isCorrect = q.isCorrect;
        }
      }

      this.currentQuestionIndex = this.questions.findIndex(q => !q.isCorrect);
      if (this.currentQuestionIndex === -1) this.currentQuestionIndex = this.questions.length;
    } 
    catch {
      localStorage.removeItem('questions');
    }
  }

  isActive(index: number): boolean {
    return index === this.currentQuestionIndex;
  }

  allCorrect(): boolean {
    return this.questions.every(q => q.isCorrect === true);
  }

  isFormatCorrect(answer: string, placeholder: string): boolean {
    if (!answer || !placeholder) return false;
    if (answer.length !== placeholder.length) return false;

    for (let i = 0; i < placeholder.length; i++) {
        const pChar = placeholder[i];
        const aChar = answer[i];

        if (pChar === '*') {
            continue;
        } 
        else if (pChar === 'X') {
            if (!/[A-Za-z]/.test(aChar)) return false;
        } 
        else if (pChar === '9') {
            if (!/[0-9]/.test(aChar)) return false;
        }
        else if (pChar === ' ') {
            if (aChar !== ' ') return false;
        }
        else {
            if (aChar !== pChar) return false;
        }
    }

    return true;
  }

  async verifyAnswerBackend(questionId: number, answer: string): Promise<boolean> {
    const backendUrl = 'http://localhost:5000/api/Answer/SendAnswer';
    try {
      const res = await fetch(backendUrl, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ id: questionId, answer })
      });

      if (res.status === 200) return true;
      if (res.status === 400) return false;
      return false;
    } 
    catch {
      return false;
    }
  }

  async getFlag() {
    this.flagLoading = true;
    this.flag = null;
    const backendUrl = 'http://localhost:5000/api/Answer/GetFlag';
    try {
      const payload = this.questions.map(q => ({ id: q.id, answer: q.answer }));

      const res = await fetch(backendUrl, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });

      if (res.status === 200) {
        const data = await res.json();
        this.flag = data?.message ?? 'Flag alınamadı';
      } else if (res.status === 400) {
        const data = await res.json();
        this.flag = data?.message ?? 'Yanlış cevaplar';
      } else {
        this.flag = 'Hata oluştu';
      }
    } catch {
      this.flag = 'Hata oluştu';
    } finally {
      this.flagLoading = false;
    }
  }
}
