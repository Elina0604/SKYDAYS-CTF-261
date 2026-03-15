import { Component } from '@angular/core';
import { Question } from '../models/Question';
import { FormsModule } from '@angular/forms';
import { CommonModule, NgFor } from '@angular/common';
import { PowService } from '../services/PowService';

@Component({
  selector: 'app-home-page',
  imports: [FormsModule, NgFor, CommonModule],
  templateUrl: './home-page.html',
  styleUrl: './home-page.css',
})
export class HomePage {
  questions: (Question & { isCorrect?: boolean })[] = [
    new Question(1, 'What is the secret route?', '/********', ''),
    new Question(2, 'What is the secret url?', 'https://hub.docker.com/r/*******/*******************/****', ''),
    new Question(3, 'What is the secret minecraft players name?', '*****', ''),
    new Question(4, 'This player has a Youtube channel, when was this channel started?', '******** *, ****', '')
  ];

  currentQuestionIndex: number = 0;
  flag: string | null = null;
  answerLoading = false;
  flagLoading = false;

  baseUrl = 'https://recon.skydays.ctf/api/Answer';

  constructor(private powService: PowService) {
    this.loadAnswers();
  }

  async checkAnswer(index: number, answer: string) {
    const question = this.questions[index];
    const userAnswer = answer.trim();

    if(!this.isFormatCorrect(userAnswer, question.placeHolder)){
      question.isCorrect = false;
      this.saveAnswers();
      return;
    }
    
    this.answerLoading = true;

    const challenge = await this.getChallenge();
    if(challenge == null){
      window.alert("Challenge okunamadı. CTF ekibinden biri ile iletişime geçiniz");
      this.saveAnswers();
      this.answerLoading = false;
      return;
    }

    const nonce = await this.powService.solve(challenge.salt, userAnswer);

    const isCorrect = await this.verifyAnswerBackend(question.id, userAnswer, challenge.salt, challenge.signature, challenge.difficulty, nonce);  
    if (isCorrect) {
      question.answer = userAnswer; 
      question.isCorrect = true;
      if (this.currentQuestionIndex === index) {
        this.currentQuestionIndex++;
      }
    } else {
      question.isCorrect = false;
    }

    this.answerLoading = false;
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

  async getChallenge(): Promise<any> {
    const backendUrl = `${this.baseUrl}/GetChallenge`;
    try {
      const res = await fetch(backendUrl);
      return await res.json();
    } 
    catch {
      return null;
    }
  }
  
  async verifyAnswerBackend(questionId: number, answer: string, salt: string, signature: string, difficulty: number, nonce: number): Promise<boolean> {
    const backendUrl = `${this.baseUrl}/SendAnswer`;
    try {
      const res = await fetch(backendUrl, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ id: questionId, answer: answer, salt: salt, signature: signature, difficulty: difficulty, nonce: nonce})
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

    const challenge = await this.getChallenge();
    if(challenge == null){
      window.alert("Challenge okunamadı. CTF ekibinden biri ile iletişime geçiniz");
      this.saveAnswers();
      return;
    }

    const nonce = await this.powService.solve(challenge.salt, this.questions[0].answer);

    const backendUrl = `${this.baseUrl}/GetFlag`;
    try {
      const payload = this.questions.map(q => ({ id: q.id, answer: q.answer, salt: challenge.salt, signature: challenge.signature, difficulty: challenge.difficulty, nonce: nonce }));
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
