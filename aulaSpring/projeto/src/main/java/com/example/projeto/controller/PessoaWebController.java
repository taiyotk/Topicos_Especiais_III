package com.example.projeto.controller;

import jakarta.validation.Valid;

import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.validation.BindingResult;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.server.ResponseStatusException;
import org.springframework.web.servlet.mvc.support.RedirectAttributes;

import com.example.projeto.model.Pessoa;
import com.example.projeto.service.PessoaService;

import org.springframework.http.HttpStatus;

@Controller
@RequestMapping("/pessoas")
public class PessoaWebController {

    private final PessoaService pessoaService;

    public PessoaWebController(PessoaService pessoaService) {
        this.pessoaService = pessoaService;
    }

    // Mapeia GET /pessoas → redireciona para /pessoas/listar
    @GetMapping
    public String index() {
        return "redirect:/pessoas/listar";
    }

    // 1. Página de cadastro
    @GetMapping("/cadastrar")
    public String exibirFormCadastro(Model model) {
        model.addAttribute("pessoa", new Pessoa());
        return "pessoas/form";
    }

    @PostMapping("/cadastrar")
    public String cadastrarPessoa(
            @Valid @ModelAttribute("pessoa") Pessoa pessoa,
            BindingResult result,
            RedirectAttributes ra) {

        if (result.hasErrors()) {
            // repopula o objeto no formulário em caso de erro
            return "pessoas/form";
        }
        pessoaService.salvarPessoa(pessoa);
        ra.addFlashAttribute("success", "Pessoa cadastrada com sucesso!");
        return "redirect:/pessoas/listar";
    }

    // 2. Página de listagem
    @GetMapping("/listar")
    public String listarPessoas(Model model) {
        model.addAttribute("lista", pessoaService.listarPessoas());
        return "pessoas/lista";
    }

    // 3. Detalhes e exclusão
    @GetMapping("/{id}")
    public String detalhesPessoa(@PathVariable Long id, Model model) {
        Pessoa p = pessoaService.buscarPorId(id)
            .orElseThrow(() -> new ResponseStatusException(
                HttpStatus.NOT_FOUND, "Pessoa não encontrada, id: " + id
            ));
        model.addAttribute("pessoa", p);
        return "pessoas/detalhe";
    }

    @PostMapping("/{id}/excluir")
    public String excluirPessoa(@PathVariable Long id, RedirectAttributes ra) {
        pessoaService.deletarPessoa(id);
        ra.addFlashAttribute("success", "Pessoa excluída com sucesso!");
        return "redirect:/pessoas/listar";
    }
}