public class PessoaService {
   private final PessoaRepository pessoaRepository;

   public PessoaService(PessoaRepository pessoaRepository){
        this.pessoaRepository = pessoaRepository;
   }

   public List<Pessoa> listarPessoas() {
        return pessoaRepository.findAll();
   }

   public Optional<Pessoa> buscarPorId(Long id) {
        return pessoaRepository.findById(id);
   }

   public Pessoa salvarPessoa(Pessoa pessoa) {
        return pessoaRepository.save(pessoa);
   }

   public void deletarPessoa(Long id) {
        pessoaRepository.deleteById(id);
   }

   
}