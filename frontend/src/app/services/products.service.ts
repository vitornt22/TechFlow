import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ProductsService {

  private apiUrl = 'http://localhost:5000/products/';

  constructor(private http: HttpClient) {}

  private getAuthHeaders(): HttpHeaders {
    const token = localStorage.getItem('access_token') || '';
    return new HttpHeaders({ 'Authorization': `Bearer ${token}` });
  }

  // Listar produtos
  getProducts(): Observable<any[]> {
    return this.http.get<any[]>(this.apiUrl, { headers: this.getAuthHeaders() });
  }

  // Adicionar produto
  addProduct(product: any): Observable<any> {
    return this.http.post<any>(this.apiUrl, product, { headers: this.getAuthHeaders() });
  }

  // Atualizar produto
  updateProduct(product: any): Observable<any> {
    return this.http.put<any>(`${this.apiUrl}${product.id}`, product, { headers: this.getAuthHeaders() });
  }

  // Deletar produto
  deleteProduct(id: number): Observable<any> {
    return this.http.delete<any>(`${this.apiUrl}${id}`, { headers: this.getAuthHeaders() });
  }
}
