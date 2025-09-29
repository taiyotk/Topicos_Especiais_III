package com.example.projeto.repository;

import org.springframework.stereotype.Repository;

@Repository
public class MensagemRepository {
    public String obterMensagem(){
        return "Mensagem do repositório";
    }
}
