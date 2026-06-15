import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";
import { Navbar } from "@/components/navbar";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "TalentGuard — Predicción de rotación de empleados",
  description:
    "Aplicación web para la predicción del riesgo de rotación de empleados usando Machine Learning. Basado en el dataset IBM HR Analytics.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html
      lang="es"
      className={`${geistSans.variable} ${geistMono.variable} h-full antialiased`}
    >
      <body className="min-h-full flex flex-col bg-[#F5F6FA]">
        <Navbar />
        <main className="flex-1 w-full max-w-6xl mx-auto px-4 sm:px-6 py-6 sm:py-8">
          {children}
        </main>
        <footer className="border-t py-4 text-center text-xs sm:text-sm text-muted-foreground">
          <div className="max-w-6xl mx-auto px-4 sm:px-6">
            TalentGuard &copy; {new Date().getFullYear()} &mdash; Proyecto
            Integrador &middot; Machine Learning
          </div>
        </footer>
      </body>
    </html>
  );
}
