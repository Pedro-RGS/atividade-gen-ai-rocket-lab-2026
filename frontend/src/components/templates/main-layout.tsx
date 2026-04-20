import { type ReactNode } from "react";
import { Header } from "../organisms/header";
import { Footer } from "../atoms/custom-footer";

interface MainLayoutProps {
  children: ReactNode;
  onSearch?: (query: string) => void;
}

export const MainLayout = ({ children, onSearch }: MainLayoutProps) => {
  return (
    <div className="min-h-screen flex flex-col bg-[#0a0a0a]">
      <Header onSearch={onSearch} />

      <main className="flex-1 w-full">{children}</main>

      <Footer />
    </div>
  );
};