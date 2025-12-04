import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router, RouterModule } from '@angular/router';
import { HttpClient, HttpClientModule, HttpHeaders } from '@angular/common/http';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterModule, HttpClientModule],
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent {
  email: string = '';
  password: string = '';

  constructor(private router: Router, private http: HttpClient) {}

  onSubmit() {
    const body = {
      email: this.email,
      password: this.password
    };

    const headers = new HttpHeaders({
      'Content-Type': 'application/json'
    });

    this.http.post(
      'http://localhost:5000/auth/login', // sem espaço!
      body,
      { headers }
    ).subscribe({
      next: (res: any) => {
        console.log('Resposta da API:', res);

        if (res.access_token) {
          localStorage.setItem('access_token', res.access_token);
          alert('Login realizado com sucesso!');
          this.router.navigate(['/products']);
        }
      },
      error: (err) => {
        console.error('ERRO NA REQ:', err);
        alert('Usuário ou senha inválidos!');
      }
    });
  }
}
