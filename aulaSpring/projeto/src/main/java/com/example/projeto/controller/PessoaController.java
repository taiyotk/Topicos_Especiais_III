import java.util.List;

import com.example.projeto.model.Pessoa;
import com.example.projeto.service.PessoaService;

public class PessoaController {
    private final PessoaService pessoaService;

    public PessoaController(PessoaService pessoaService){
          this.pessoaService = pessoaService;
    }

    @Getmapping
    public List<Pessoa> listarPessoas() {
          return pessoaService.listarPessoas();
    }

    @GetMapping("/{id}")
    public ResponseEntity<Pessoa> buscarPessoa(@PathVariable Long id) {
        return pessoaService.buscarPorId(id)
            .map(ResponseEntity::ok)
            .orElse(ResponseEntity.notFound().build());
    }

    public Pessoa criarPessoa(@PathVariable Pessoa pessoa) {
        return pessoaService.salvarPessoa(pessoa);

    }

    public ResponseEntity<Void> deletarPessoa(@PathVariable Long id) {
        pessoaService.deletarPessoa(id);
        return ResponseEntity.noContent().build();
    }

}