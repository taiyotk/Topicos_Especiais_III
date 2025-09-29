package com.example.projeto.service;

import org.springframework.stereotype.Service;
import com.example.projeto.repository.ProdutoRepository;
import com.example.projeto.model.Produto;

import java.util.List;
import java.util.Optional;

@Service
public class ProdutoService{
    private final ProdutoRepository produtoRepository;

    public ProdutoService(ProdutoRepository produtoRepository){
        this.produtoRepository = produtoRepository;
    }

    public List<Produto> listarProdutos(){
        return produtoRepository.findAll();
    }

    public Optional<Produto> buscarPorId(Long id){
        return produtoRepository.findById(id);
    }

    public Produto salvarProduto(Produto produto){
        return produtoRepository.save(produto);
    }

    public void deletarProduto(Long id){
        produtoRepository.deleteById(id);
    }
}