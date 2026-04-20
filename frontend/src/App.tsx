import { Route, Routes } from 'react-router-dom'
import { HomePage } from "./pages/home-page";
import { ProductPage } from "./pages/product-page"
import { CreateProductPage } from "./pages/create-product";
import { EditProductPage } from "./pages/edit-product";

function App() {

  return (
    <>
      <main>
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/product/:id" element={<ProductPage />} />
          <Route path="/product/create" element={<CreateProductPage />} />
          <Route
            path="/admin/editar-produto/:id"
            element={<EditProductPage />}
          />
        </Routes>
      </main>
    </>
  );
}

export default App
