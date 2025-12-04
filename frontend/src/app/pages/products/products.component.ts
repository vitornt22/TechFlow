import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router, RouterModule } from '@angular/router';
import { ProductsService } from '../../services/products.service';
import { HttpClientModule } from '@angular/common/http';

interface Product {
  id?: number;
  name: string;
  brand: string;
  value: number;
}

@Component({
  selector: 'app-products',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterModule, HttpClientModule],
  templateUrl: './products.component.html',
  styleUrls: ['./products.component.css'],
})
export class ProductsComponent {
  products: Product[] = [];
  currentProduct: Product = { name: '', brand: '', value: 0 };
  searchTerm: string = '';
  isEditing: boolean = false;

  constructor(private router: Router, private productService: ProductsService) {
    this.loadProducts();
  }

  loadProducts() {
    this.productService.getProducts().subscribe({
      next: (res: any[]) => {
        this.products = res.map(p => ({
          id: p.id,
          name: p.nome,
          brand: p.marca,
          value: Number(p.valor),
        }));
      },
      error: (err) => {
        if (err.status === 401) {
          alert('Sessão expirada. Faça login novamente.');
          localStorage.removeItem('access_token');
          this.router.navigate(['/login']);
        } else {
          console.error('Erro ao carregar produtos:', err);
          alert('Erro ao buscar produtos!');
        }
      }
    });
  }

  logout() {
    if (!confirm("Tem certeza que deseja sair?")) return;
    localStorage.removeItem('access_token');
    alert('Logout realizado com sucesso!');
    this.router.navigate(['/']);
  }

  addOrUpdateProduct() {
    const body = {
      nome: this.currentProduct.name,
      marca: this.currentProduct.brand,
      valor: this.currentProduct.value,
    };

    if (this.isEditing && this.currentProduct.id) {
      // Atualiza produto
      this.productService.updateProduct({ id: this.currentProduct.id, ...body }).subscribe({
        next: (res: any) => {
          if (res?.msg) alert(res.msg);
          this.isEditing = false;
          this.currentProduct = { name: '', brand: '', value: 0 };
          this.loadProducts();
        },
        error: (err) => {
          console.error(err);
          alert('Erro ao atualizar produto');
        }
      });
    } else {
      // Adiciona produto
      this.productService.addProduct(body).subscribe({
        next: (res: any) => {
          if (res?.msg) alert(res.msg);
          this.currentProduct = { name: '', brand: '', value: 0 };
          this.loadProducts();
        },
        error: (err) => {
          console.error(err);
          alert('Erro ao adicionar produto');
        }
      });
    }
  }

  editProduct(product: Product) {
    this.currentProduct = { ...product };
    this.isEditing = true;
  }

  deleteProduct(id?: number) {
    if (!id) return;
    if (!confirm("Deseja realmente excluir este produto?")) return;

    this.productService.deleteProduct(id).subscribe({
      next: (res: any) => {
        if (res?.msg) alert(res.msg);
        this.loadProducts();
      },
      error: (err) => {
        console.error(err);
        alert("Erro ao remover produto");
      }
    });
  }

  filteredProducts() {
    return this.products.filter(p =>
      p.name.toLowerCase().includes(this.searchTerm.toLowerCase()) ||
      p.brand.toLowerCase().includes(this.searchTerm.toLowerCase())
    );
  }
}
