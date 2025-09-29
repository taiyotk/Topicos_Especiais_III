package com.example.projeto.service;

import org.springframework.stereotype.Service;
import com.example.projeto.repository.PessoaRepository;
import com.example.projeto.model.Pessoa;

import java.util.List;
import java.util.Optional;

@Service
public class PessoaService{
    private final PessoaRepository pessoaRepository;

    public PessoaService(PessoaRepository pessoaRepository){
        this.pessoaRepository = pessoaRepository;
    }

    public List<Pessoa> listarPessoas(){
        return pessoaRepository.findAll();
    }

    public Optional<Pessoa> buscarPorId(Long id){
        return pessoaRepository.findById(id);
    }

    public Pessoa salvarPessoa(Pessoa pessoa){
        return pessoaRepository.save(pessoa);
    }

    public void deletarPessoa(Long id){
        pessoaRepository.deleteById(id);
    }
}