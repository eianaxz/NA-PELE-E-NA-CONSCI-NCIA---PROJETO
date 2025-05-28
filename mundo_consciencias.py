import tkinter as tk
from tkinter import ttk, messagebox
import os

class MundoConscienciaElias:
    def __init__(self, root, user_data, content_frame, menu_app):
        self.root = root
        self.user_data = user_data
        self.content_frame = content_frame
        self.menu_app = menu_app
        self.current_choice_path = []
        self.story_state = "intro"
        self.player_attributes = {
            "Justice": 0,
            "Reputation": 0,
            "Empathy": 0,
            "Stress": 0
        }
        self.story = self.setup_story_structure()
        self.style = ttk.Style()
        self.apply_styles()

    def apply_styles(self):
        """Aplica estilos personalizados para uma interface mais moderna."""
        self.style.theme_use('clam')
        self.root.configure(bg="#222222")
        self.content_frame.configure(bg="#222222")

        self.style.configure("TLabel", background="#222222",
                       foreground="#E0E0E0", font=("Consolas", 22, "bold"))
        self.style.configure("Story.TLabel", background="#222222",
                       foreground="#D0D0D0", font=("Consolas", 13))
        self.style.configure("Attribute.TLabel", background="#222222",
                       foreground="#E0E0E0", font=("Consolas", 12))

        self.style.configure("Choice.TButton",
                       font=("Consolas", 12),
                       background="#444444",
                       foreground="#EEEEEE",
                       relief="flat",
                       padding=10,
                       borderwidth=0)

        self.style.map("Choice.TButton",
                  background=[('active', '#555555'), ('pressed', '#333333')],
                  foreground=[('active', '#FFFFFF'), ('pressed', '#FFFFFF')])

        self.style.configure("Action.TButton",
                       font=("Consolas", 14, "bold"),
                       background="#007ACC",
                       foreground="white",
                       relief="flat",
                       padding=12,
                       borderwidth=0)

        self.style.map("Action.TButton",
                  background=[('active', '#0099EE'), ('pressed', '#0055AA')],
                  foreground=[('active', '#FFFFFF'), ('pressed', '#FFFFFF')])

        self.style.configure("Back.TButton",
                       font=("Consolas", 12),
                       background="#FF5733",
                       foreground="white",
                       relief="flat",
                       padding=8,
                       borderwidth=0)

        self.style.map("Back.TButton",
                  background=[('active', '#FF7A55'), ('pressed', '#CC4028')],
                  foreground=[('active', '#FFFFFF'), ('pressed', '#FFFFFF')])

        self.style.configure("Secondary.TButton",
                       font=("Helvetica", 11),
                       foreground="white",
                       background="#607D8B",
                       padding=8,
                       bordercolor="#607D8B")
        
        self.style.map("Secondary.TButton",
                  background=[('active', '#546E7A')],
                  relief=[('pressed', 'sunken'), ('!pressed', 'raised')])

    
    def setup_story_structure(self):
        """Estrutura hierárquica da história baseada no PDF"""
        return {
            "intro": {
                "title": "⚖️ O JULGAMENTO DE ELIAS ⚖️",
                "text": """Você é juiz há 12 anos. É conhecido por sua imparcialidade, mas também por sua frieza técnica. Hoje, você encara um dos julgamentos mais controversos da sua carreira: Elias, um jovem negro e professor de filosofia, é preso acusado de envolvimento em um assalto violento que deixou uma vítima em coma. Não há provas físicas contra ele — nenhuma digital, nenhuma arma, nenhum DNA. Apenas o depoimento de uma testemunha, que afirma tê-lo visto no local do crime. A pressão da mídia e da população é grande. Como juiz, você precisa decidir o destino de Elias. A sociedade quer justiça. Mas será que justiça é o mesmo que punição?""",
                "choices": [
                    ("📜 Seguir com o julgamento mesmo sem provas, confiando no processo.", "1"),
                    ("⏳ Adiar o julgamento até surgirem provas mais concretas.", "2"),
                    ("❌ Arquivar o caso por falta de provas e libertar Elias.", "3")
                ],
                # Indica qual container de escolhas estas escolhas levam
                "next_container_key": "choices_lvl1"
            },
            "choices_lvl1": {  # Container das escolhas resultantes da intro
                "1": {
                    "title": "👁️‍🗨️ Seguir com o julgamento",
                    "text": """O tribunal se enche. O público vibra como se estivesse num espetáculo. Seu rosto estampa jornais como símbolo de ação firme contra o crime. Porém, durante a noite, você recebe um e-mail anônimo: "E se fosse você no banco dos réus?" A pressão se transforma em inquietação interna. Agora você como juiz recebe mais 3 escolhas de decisões que pode tomar, o que você escolhe?""",
                    "choices": [
                        ("🗣️ Ouvir apenas testemunhas da acusação.", "1.1"),
                        ("🤝 Solicitar novas testemunhas imparciais.", "1.2"),
                        ("🚫 Impedir novas evidências após a abertura do julgamento.", "1.3")
                    ],
                    "next_container_key": "choices_lvl2_1"
                },
                "2": {
                    "title": "⏸️ Adiar o julgamento",
                    "text": """O povo protesta: "Covarde!" Mas uma defensora pública sussurra: "Você está protegendo a justiça." Nos bastidores, você inicia uma investigação paralela. E, mais três decisões aparecem:""",
                    "choices": [
                        ("🔎 Enviar investigadores para reabrirem o caso.", "2.1"),
                        ("🎙️ Realizar uma audiência pública sobre o caso.", "2.2"),
                        ("📚 Revisar o histórico de Elias em busca de possíveis motivações.", "2.3")
                    ],
                    "next_container_key": "choices_lvl2_2"
                },
                "3": {
                    "title": "📂 Arquivar o caso",
                    "text": """Você decide arquivar o caso por falta de provas suficientes. """,
                    "choices": [
                        ("📢 Fazer um pronunciamento explicando a decisão.", "3.1"),
                        ("🤫 Manter silêncio para evitar retaliações.", "3.2"),
                        ("🤝 Conversar com a família da vítima para explicar a falta de provas.", "3.3")
                    ],
                    "next_container_key": "choices_lvl2_3"
                }
            },
            "choices_lvl2_1": {  # Container para as escolhas 1.1, 1.2, 1.3
                "1.1": {
                    "title": "🔊 Ouvir apenas testemunhas da acusação",
                    "text": """Ao optar por ouvir somente as testemunhas da acusação, o tribunal recebe depoimentos contundentes contra Elias. A defesa reclama de parcialidade e pede reconsideração, mas sua decisão mantém o foco unilateral. A população fica dividida: alguns clamam por justiça rápida, enquanto outros acusam o sistema de ser injusto e precipitado. Elias parece cada vez mais desesperado diante da falta de uma defesa justa. Como juiz, você tem mais um último desafio: Tomar a decisão final acerca do julgamento de Elias, e agora, o que você faz?""",
                    "choices": [
                        ("⚖️ Manter a decisão e condenar Elias com base nos depoimentos apresentados.", "1.1.1"),
                        ("🚪 Permitir que a defesa apresente suas testemunhas para garantir um julgamento mais justo.", "1.1.2"),
                        ("🔄 Reabrir o inquérito para buscar novas provas que possam confirmar ou refutar os depoimentos.", "1.1.3")
                    ],
                    "next_container_key": "final_outcomes"
                },
                "1.2": {
                    "title": "🤝 Solicitar novas testemunhas imparciais",
                    "text": """Você decide suspender temporariamente o julgamento e exige a convocação de testemunhas que não estejam ligadas nem à acusação nem à defesa. Isso gera tensão no tribunal. A mídia elogia sua tentativa de neutralidade, mas os advogados da acusação alegam que isso enfraquece a posição deles. Após alguns dias, três novas testemunhas são localizadas: um segurança do local do crime, um vizinho que escutou gritos naquela noite e um entregador que passava na rua. Essas novas testemunhas trazem versões que contradizem partes da acusação, mas também deixam dúvidas no ar. O julgamento se torna ainda mais delicado. Agora, surge uma nova responsabilidade para você: Decidir quais outros caminhos esse julgamento deve tomar. O que você escolhe?""",
                    "choices": [
                        ("📝 Registrar os novos depoimentos e levar o julgamento direto à decisão final.", "1.2.1"),
                        ("🔬 Solicitar perícia técnica complementar para verificar detalhes apontados nas novas falas.", "1.2.2"),
                        ("🗳️ Propor um júri popular para que a decisão final reflita a visão coletiva da sociedade.", "1.2.3")
                    ],
                    "next_container_key": "final_outcomes"
                },
                "1.3": {
                    "title": "🚫 Impedir novas evidências após a abertura do julgamento",
                    "text": """Você decide que o julgamento seguirá apenas com as provas apresentadas inicialmente. A defesa protesta energicamente, afirmando que novas evidências poderiam provar a inocência de Elias. A opinião pública explode - alguns elogiam sua firmeza e defesa da ordem processual; outros o acusam de estar ignorando o direito à verdade. Um jornalista investigativo revela que houve uma denúncia anônima com possíveis provas novas, mas você recusa aceitá-las oficialmente, alegando que o julgamento já está em curso e deve ser finalizado. O clima é tenso. Elias parece cada vez mais fragilizado.""",
                    "choices": [
                        ("🔒 Condenar Elias com as provas existentes, mantendo a firmeza na decisão.", "1.3.1"),
                        ("⚖️ Considerar a possibilidade de reavaliar, mas manter a decisão inicial para evitar atrasos.", "1.3.2"),
                        ("✨ Suspender o julgamento para buscar novas evidências, mesmo contra a decisão anterior.", "1.3.3")
                    ],
                    "next_container_key": "final_outcomes"
                }
            },
            "choices_lvl2_2": {  # Container para as escolhas 2.1, 2.2, 2.3
                "2.1": {
                    "title": "🔎 Enviar investigadores para reabrirem o caso",
                    "text": """Você determina que o caso seja reaberto para investigação. Dois detetives independentes são convocados. Dias depois, descobrem inconsistências no depoimento da principal testemunha da acusação e também encontram imagens de uma câmera de segurança mal analisada anteriormente, que pode mudar o rumo do processo. A mídia começa a cobrir o caso com mais atenção, e a opinião pública começa a se dividir entre "Elias pode ser inocente" e "Estão querendo livrar um criminoso". O tempo para julgamento é estendido, gerando pressão política e institucional sobre você.""",
                    "choices": [
                        ("🚨 Pressionar para a prisão do verdadeiro culpado e reabilitar Elias publicamente.", "2.1.1"),
                        ("🤫 Manter a discrição, concluindo o caso sem alardes para evitar mais perturbações.", "2.1.2"),
                        ("🏛️ Usar o caso como exemplo para promover reformas no sistema judiciário.", "2.1.3")
                    ],
                    "next_container_key": "final_outcomes"
                },
                "2.2": {
                    "title": "🎙️ Realizar uma audiência pública sobre o caso",
                    "text": """Você decide abrir uma audiência pública, permitindo que o caso de Elias seja debatido com transparência. Familiares da vítima e do acusado, representantes da sociedade civil, juristas e jornalistas participam. A audiência se torna um evento de grande repercussão. Durante a sessão, surgem dúvidas importantes sobre a coerência da investigação original. A sociedade pressiona por justiça, mas com equilíbrio. A opinião pública se divide: alguns te veem como corajoso e transparente; outros acham que a justiça está se tornando um espetáculo.""",
                    "choices": [
                        ("❤️ Considerar a opinião pública e julgar Elias com base na comoção popular.", "2.2.1"),
                        ("📈 Ignorar a pressão e focar apenas nas evidências técnicas para a decisão.", "2.2.2"),
                        ("🕵️ Suspender a audiência para realizar novas investigações sobre os depoimentos.", "2.2.3")
                    ],
                    "next_container_key": "final_outcomes"
                },
                "2.3": {
                    "title": "📚 Revisar o histórico de Elias em busca de possíveis motivações",
                    "text": """Você decide solicitar uma investigação completa sobre o passado de Elias: antecedentes criminais, histórico escolar, profissional e relações sociais. Descobre que ele teve um desentendimento com a vítima há alguns anos, mas também que nunca teve envolvimento com atividades ilegais. Relatórios sociais mostram que ele era visto como alguém calmo e trabalhador, embora tenha sofrido episódios de discriminação racial e perseguição policial injustificada em seu bairro. A imprensa começa a questionar se a justiça está usando o passado dele para justificar uma acusação sem provas.""",
                    "choices": [
                        ("👊 Confrontar as autoridades locais sobre a possível perseguição política contra Elias.", "2.3.1"),
                        ("🕵️‍♀️ Manter a discrição e continuar investigando internamente para evitar escândalos.", "2.3.2"),
                        ("📰 Divulgar as novas informações para a imprensa para pressionar por uma investigação externa.", "2.3.3")
                    ],
                    "next_container_key": "final_outcomes"
                }
            },
            "choices_lvl2_3": {  # Container para as escolhas 3.1, 3.2, 3.3
                "3.1": {
                    "title": "📢 Fazer um pronunciamento explicando a decisão",
                    "text": """Você decide se posicionar publicamente. Em rede nacional, comunica com firmeza que o caso foi arquivado por falta de provas e que a justiça não pode se basear em suposições. No pronunciamento, você destaca a importância da presunção de inocência e do respeito aos direitos humanos. O país se divide: parte da população apoia sua coragem; outra parte o acusa de estar "protegendo criminosos" e enfraquecendo a justiça. A imprensa pressiona, a promotoria recorre, e protestos começam a surgir nas redes e nas ruas.""",
                    "choices": [
                        ("🔐 Solicitar proteção para Elias e sua família", "3.1.1"),
                        ("🕵 Criar uma força-tarefa independente para investigar o caso por fora", "3.1.2"),
                        ("🧾 Reabrir o caso discretamente após novas denúncias anônimas", "3.1.3")
                    ],
                    "next_container_key": "final_outcomes"
                },
                "3.2": {
                    "title": "🤫 Manter silêncio para evitar retaliações",
                    "text": """Você decide não se pronunciar publicamente após arquivar o caso de Elias. A mídia começa a especular os motivos do silêncio. Grupos ativistas o criticam por não dar satisfação à sociedade, enquanto outros o elogiam por evitar politização. Elias, mesmo livre, enfrenta hostilidade em seu bairro e tem dificuldade para retomar a vida. O clima é de tensão. Seu silêncio vira símbolo de prudência para alguns — e de omissão para outros.""",
                    "choices": [
                        ("📞 Entrar em contato diretamente com a família de Elias", "3.2.1"),
                        ("📄 Redigir um relatório confidencial explicando sua decisão, a ser usado apenas se necessário", "3.2.2"),
                        ("🗂 Encaminhar discretamente o caso para um grupo de direitos humanos investigar por fora", "3.2.3")
                    ],
                    "next_container_key": "final_outcomes"
                },
                "3.3": {
                    "title": "🤝 Conversar com a família da vítima para explicar a falta de provas",
                    "text": """Você marca uma reunião privada com os pais da vítima. Eles estão emocionalmente abalados e com sede de justiça. Ao explicar que o caso foi arquivado por falta de provas concretas, a família reage com dor, revolta e incompreensão. Acusam o sistema de ser falho e juram buscar justiça por conta própria. A notícia da conversa vaza para a mídia. O clima se torna ainda mais delicado: agora, além da pressão social, há risco de retaliação contra Elias por parte de simpatizantes da vítima.""",
                    "choices": [
                        ("⚠️ Oferecer proteção legal e psicológica à família da vítima", "3.3.1"),
                        ("󰳌 Encaminhar a família para abertura de um processo cível paralelo", "3.3.2"),
                        ("🧯 Intermediar um encontro entre a família da vítima e Elias (caso ele aceite)", "3.3.3")
                    ],
                    "next_container_key": "final_outcomes"
                }
            },
            "final_outcomes": {  # O container que agrupa todos os desfechos finais
                "1.1.1": {
                    "title": "❌ Condenação Injusta ❌",
                    "text": """Elias é condenado à prisão perpétua. Anos depois, novas evidências surgem provando sua inocência, mas ele já está cumprindo pena. A sociedade questiona o sistema judicial, e sua reputação como juiz fica gravemente manchada. Você passa a sofrer ataques públicos e internos por ter ignorado a possibilidade de injustiça.""",
                    "attributes": {"Justice": -8, "Reputation": -10, "Empathy": -5, "Stress": 12}
                },
                "1.1.2": {
                    "title": "✅ Absolvição com Integridade ✅",
                    "text": """A defesa traz testemunhas que apontam falhas nas acusações, gerando dúvidas razoáveis no júri. Elias é absolvido, e você é reconhecido por garantir o direito ao contraditório, preservando os valores da justiça. No entanto, você enfrenta críticas por atrasar o processo.""",
                    "attributes": {"Justice": 7, "Reputation": 8, "Empathy": 6, "Stress": 4}
                },
                "1.1.3": {
                    "title": "🔥 Descoberta da Corrupção 🔥",
                    "text": """A investigação revela uma conspiração dentro da polícia, forjando provas contra Elias. O caso se torna um escândalo nacional, e você é visto como um símbolo da luta contra a corrupção. Elias é libertado, e sua carreira judicial se fortalece, mas você enfrenta ameaças e pressões constantes.""",
                    "attributes": {"Justice": 10, "Reputation": 12, "Empathy": 8, "Stress": 10}
                },
                "1.2.1": {
                    "title": "✨ Justiça Prevalecida ✨",
                    "text": """Você considera os relatos das testemunhas imparciais e decide que há dúvida razoável. Elias é absolvido. No entanto, meses depois, outra pessoa confessa o crime com detalhes. Você é elogiado por ter evitado uma injustiça, mas também criticado por não ter ido mais a fundo. A sociedade se divide: metade reconhece sua coragem, metade chama de "juiz frouxo".""",
                    "attributes": {"Justice": 6, "Reputation": 4, "Empathy": 7, "Stress": 5}
                },
                "1.2.2": {
                    "title": "🏆 O Juiz Honesto 🏆",
                    "text": """A perícia revela que Elias não estava na cena do crime, e que houve manipulação de dados no relatório original da polícia. Você encaminha o caso ao Ministério Público e uma rede de corrupção policial é descoberta. Elias é libertado, e você se torna símbolo da justiça meticulosa. Mas sofre retaliações e ameaças.""",
                    "attributes": {"Justice": 10, "Reputation": 9, "Empathy": 8, "Stress": 10}
                },
                "1.2.3": {
                    "title": "📉 Decisão Popular e Injusta 📉",
                    "text": """O júri ouve todas as versões e decide pela condenação de Elias. Mais tarde, novas provas revelam que o júri foi influenciado por um vazamento de informações falsas nas redes sociais. Elias é inocente. Você se vê arrependido por ter delegado a decisão sem garantir segurança plena do processo. Sua imagem sofre, e você passa a repensar o papel do juiz na mediação da verdade.""",
                    "attributes": {"Justice": -8, "Reputation": -7, "Empathy": -7, "Stress": 8}  # Ajustado para o range, dado que não há valores específicos para este no PDF.
                },
                "1.3.1": {
                    "title": "⚖️ Firmeza Questionável ⚖️",
                    "text": """Elias é condenado. Sem chance de defesa atualizada, ele é levado para a prisão. Meses depois, a denúncia anônima leva à prisão do verdadeiro culpado um parente da vítima que confessou em troca de delação premiada. A sua imagem como juiz entra em colapso. Movimentos sociais protestam, e sua carreira entra em declínio.""",
                    "attributes": {"Justice": -9, "Reputation": -10, "Empathy": -5, "Stress": 12}
                },
                "1.3.2": {
                    "title": "⚠️ A Incerteza da Decisão ⚠️",
                    "text": """Você conclui o julgamento com base nas provas antigas, mas permite que os autos fiquem abertos para recurso. Elias é condenado, mas sua defesa entra com novo processo dias depois. A apelação revela a inocência dele, e ele é libertado. Você é criticado por não ter agido antes, mas elogiado por ter deixado espaço para a revisão.""",
                    "attributes": {"Justice": 2, "Reputation": -3, "Empathy": 4, "Stress": 8}
                },
                "1.3.3": {
                    "title": "🌟 A Coragem da Verdade 🌟",
                    "text": """Você fecha completamente a porta para qualquer novo elemento. Elias é condenado. A denúncia anônima se torna pública pelas redes sociais e imprensa. Um escândalo explode. Você sofre um processo por violação dos direitos constitucionais do réu. Seu nome é usado em campanhas contra injustiças judiciais. Mesmo assim, você defende sua decisão até o fim.""",
                    "attributes": {"Justice": -12, "Reputation": -15, "Empathy": -8, "Stress": 15}
                },
                "2.1.1": {
                    "title": "🦸‍♂️ Ícone da Justiça 🦸‍♂️",
                    "text": """A perícia comprova que Elias não estava na cena do crime, e a gravação mostra outro homem, posteriormente identificado como o verdadeiro autor. A acusação desmorona. Elias é libertado e você é homenageado por sua decisão de aprofundar a verdade, mesmo sob pressão. O processo vira exemplo em faculdades de Direito.""",
                    "attributes": {"Justice": 10, "Reputation": 8, "Empathy": 6, "Stress": 4}
                },
                "2.1.2": {
                    "title": "🤫 Justiça Silenciosa 🤫",
                    "text": """A testemunha entra em contradição e, pressionada, admite que foi coagida pela polícia para mentir. Uma investigação maior é aberta, revelando manipulação de provas. Você suspende o julgamento e solicita revisão total do processo. Elias é libertado, mas a crise institucional gera ataques à sua conduta. Mesmo assim, defensores dos direitos humanos o apoiam fortemente.""",
                    "attributes": {"Justice": 9, "Reputation": 3, "Empathy": 7, "Stress": 9}
                },
                "2.1.3": {
                    "title": "✊ Agente de Mudança ✊",
                    "text": """Você solicita a suspensão do julgamento e proteção especial ao réu. Isso causa comoção setores da sociedade veem sua decisão como prudente, outros como provocativa. Uma semana depois, o verdadeiro culpado confessa o crime para aliviar sua consciência. Elias é libertado, mas sua imagem permanece manchada por ter sido preso e acusado injustamente por tanto tempo.""",
                    "attributes": {"Justice": 7, "Reputation": -2, "Empathy": 9, "Stress": 6}
                },
                "2.2.1": {
                    "title": "🎭 Justiça Emocional 🎭",
                    "text": """Elias faz um discurso emocionado. Ele expõe falhas do processo, fala de sua vida, de como perdeu o emprego, o respeito da comunidade e a paz. O público se comove. Uma nova testemunha que estava calada por medo decide falar, revelando que Elias não estava na cena do crime. A investigação reabre, ele é inocentado. Sua fala viraliza como símbolo contra erros judiciais.""",
                    "attributes": {"Justice": 8, "Reputation": 9, "Empathy": 10, "Stress": 6}
                },
                "2.2.2": {
                    "title": "🛡️ Integridade Inabalável 🛡️",
                    "text": """O comitê formado por juristas e especialistas encontra diversas irregularidades no processo, incluindo provas forjadas. Você é parabenizado por buscar isenção. A promotoria é investigada, Elias é libertado e recebe uma indenização do Estado. Você é visto como exemplo de ética judicial.""",
                    "attributes": {"Justice": 10, "Reputation": 7, "Empathy": 8, "Stress": 5}
                },
                "2.2.3": {
                    "title": "👑 Herói da Verdade 👑",
                    "text": """Ao encerrar a audiência, parte da população se frustra por sentir que a discussão foi interrompida. No julgamento, as provas continuam frágeis, mas você sente-se pressionado a seguir com o rito. Elias é condenado. Meses depois, uma denúncia anônima aponta outro suspeito, mas o caso já está encerrado. A credibilidade do processo é duramente questionada.""",
                    "attributes": {"Justice": -4, "Reputation": -5, "Empathy": -2, "Stress": 10}
                },
                "2.3.1": {
                    "title": "🔥 Confronto Corajoso 🔥",
                    "text": """O psicólogo avalia Elias como emocionalmente estável, com sinais de trauma recente pela prisão injusta. A avaliação desmonta a tese da promotoria sobre “comportamento agressivo oculto”. A defesa solicita a anulação do processo e você a acata. Elias é libertado, e sua imagem começa a ser restaurada com o apoio de psicólogos, juristas e movimentos sociais.""",
                    "attributes": {"Justice": 9, "Reputation": 6, "Empathy": 9, "Stress": 5}
                },
                "2.3.2": {
                    "title": "🕵️‍♂️ Investigação Discreta 🕵️‍♂️",
                    "text": """O histórico é usado no tribunal, mas parte da sociedade considera essa atitude preconceituosa. Não há provas materiais, mas o histórico negativo do conflito com a vítima influencia o júri, que o considera culpado. Elias é condenado, e mais tarde descobre-se que o verdadeiro autor do crime fugiu do país. A sua reputação como juiz é seriamente abalada.""",
                    "attributes": {"Justice": -5, "Reputation": -7, "Empathy": -4, "Stress": 10}
                },
                "2.3.3": {
                    "title": "📢 O Legado do Juiz 📢",
                    "text": """Você descobre que a vítima tinha envolvimento com um grupo de extorsão na região e que Elias havia sido uma das pessoas que se recusaram a pagar esse grupo. Essa descoberta muda completamente a narrativa: Elias passa a ser visto como possível alvo de uma armação. Uma nova investigação é aberta, o caso é suspenso, e Elias é libertado com apoio popular.""",
                    "attributes": {"Justice": 10, "Reputation": 9, "Empathy": 7, "Stress": 3}
                },
                "3.1.1": {
                    "title": "🤝 Compaixão e Lei 🤝",
                    "text": """Elias e seus familiares passam a receber ameaças. Com sua intervenção, a segurança deles é reforçada, evitando uma tragédia. Isso é bem visto por grupos de direitos humanos, mas criticado por setores conservadores. Um tempo depois, uma testemunha revela que a denúncia contra Elias foi fabricada. O verdadeiro culpado é preso, e sua postura preventiva é exaltada.""",
                    "attributes": {"Justice": 8, "Reputation": 7, "Empathy": 9, "Stress": 6}
                },
                "3.1.2": {
                    "title": "📚 O Educador da Justiça 📚",
                    "text": """A força-tarefa é bem recebida pela sociedade. Sem vínculo direto com o Judiciário, ela consegue novas evidências — inclusive um vídeo comprometedor de outro suspeito. Elias é oficialmente inocentado. Sua decisão de arquivar o processo é vista agora como prudente, e sua reputação cresce como a de um juiz ético e estratégico.""",
                    "attributes": {"Justice": 10, "Reputation": 10, "Empathy": 7, "Stress": 4}
                },
                "3.1.3": {
                    "title": "⚖️ Foco na Eficiência ⚖️",
                    "text": """Você age por fora do protocolo. As novas denúncias não são confirmadas, e seu ato é descoberto pela promotoria. Você é acusado de abuso de autoridade por tentar agir secretamente após arquivar o caso formalmente. Apesar da boa intenção, a mancha no seu histórico pesa. Elias continua em liberdade, mas você é afastado temporariamente do cargo.""",
                    "attributes": {"Justice": 4, "Reputation": -6, "Empathy": 6, "Stress": 9}
                },
                "3.2.1": {
                    "title": "🌪️ Silêncio e Desconfiança 🌪️",
                    "text": """Você conversa com a família de Elias. Eles estão assustados e desamparados. Sua postura humana e solidária os reconforta. Eles ganham confiança e coragem para falar publicamente. Isso muda a narrativa: Elias dá entrevista, conta sua versão e a sociedade começa a enxergar o erro. Sua empatia, ainda que silenciosa, causa grande impacto.""",
                    "attributes": {"Justice": 7, "Reputation": 6, "Empathy": 10, "Stress": 4}
                },
                "3.2.2": {
                    "title": "🤝 Apoio nos Bastidores 🤝",
                    "text": """Meses depois, você é questionado por um conselho superior. O relatório detalhado protege você de punições e mostra que a decisão de arquivar foi técnica, não política. O caso volta aos holofotes, mas você se mantém firme. Elias continua livre, e a investigação é reaberta por outra vara judicial. Sua reputação como um juiz estrategista cresce nos bastidores.""",
                    "attributes": {"Justice": 9, "Reputation": 8, "Empathy": 6, "Stress": 3}
                },
                "3.2.3": {
                    "title": "📉 Recuperação Tardía 📉",
                    "text": """O grupo assume o caso e descobre provas que haviam sido ignoradas. A nova investigação isenta Elias e expõe falhas policiais. Seu nome não aparece diretamente, mas jornalistas descobrem sua influência silenciosa. O público o enxerga como um juiz que age com sabedoria e sensibilidade. Elias passa a colaborar com o grupo, tornando-se ativista.""",
                    "attributes": {"Justice": 10, "Reputation": 9, "Empathy": 8, "Stress": 2}
                },
                "3.3.1": {
                    "title": "🌟 A Humanidade da Justiça 🌟",
                    "text": """O apoio institucional oferecido ajuda a família a lidar com o luto e canalizar a dor de forma construtiva. Eles participam de audiências públicas, criam um grupo de apoio a vítimas e passam a lutar por melhorias no sistema investigativo. Elias permanece livre e em segurança. Sua atuação é vista como firme, porém sensível.""",
                    "attributes": {"Justice": 9, "Reputation": 7, "Empathy": 10, "Stress": 5}
                },
                "3.3.2": {
                    "title": "🔎 O Caminho Contínuo da Justiça 🔎",
                    "text": """A família acata a sugestão e move um processo cível, acusando o Estado de omissão. Isso levanta debates importantes sobre falhas processuais. Você é chamado para prestar depoimento, mas seu equilíbrio e argumentação são elogiados. A decisão judicial é mantida, mas o caso vira referência para reformas jurídicas.""",
                    "attributes": {"Justice": 10, "Reputation": 8, "Empathy": 7, "Stress": 6}
                },
                "3.3.3": {
                    "title": "🔒 Discrição e Confiança 🔒",
                    "text": """Apesar da tensão inicial, o encontro ocorre com apoio de mediadores. Elias expressa empatia e dor pelas acusações que sofreu, enquanto os pais da vítima, mesmo inconformados, enxergam um ser humano diante deles, não um monstro. A conversa não resolve tudo, mas abre espaço para uma nova narrativa. A imprensa cobre o evento e elogia sua coragem.""",
                    "attributes": {"Justice": 8, "Reputation": 10, "Empathy": 10, "Stress": 7}

                }
            }

        }

    def clear_content_frame(self):
        """Limpa todo o conteúdo do frame principal."""
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def show_story_screen(self):
        """Mostra a tela da história atual baseada no estado."""
        self.clear_content_frame()

        if self.story_state == "final_outcomes":
            self.show_final_outcome()
        else:
            self.show_choices_screen()

    def create_choice_button(self, parent_frame, text, choice_key):
        """Cria um botão de escolha personalizado e interativo."""
        button = ttk.Button(parent_frame, text=text, style="Choice.TButton")
        button.pack(pady=7, padx=50, anchor=tk.W, fill=tk.X)
        button.configure(command=lambda k=choice_key,
                         b=button: self.on_choice_button_click(k, b))
        return button

    def on_choice_button_click(self, choice_key, clicked_button):
        """Atualiza a variável de escolha e visualmente marca o botão selecionado."""
        self.choice_var.set(choice_key)
        for btn in self.choice_buttons:
            if btn == clicked_button:
                btn.configure(style="Action.TButton")
            else:
                btn.configure(style="Choice.TButton")

    def show_choices_screen(self):
        """Mostra a tela de escolhas e texto para os estados intermediários ou intro."""
        current_data = self.get_current_story_segment()

        if not current_data:
            messagebox.showerror(
                "Erro de Jogo", "Segmento da história não encontrado. Reiniciando.")
            self.restart_game()
            return

        title_label = ttk.Label(
            self.content_frame, text=current_data["title"], style="TLabel")
        title_label.pack(pady=30)

        text_frame = tk.Frame(self.content_frame, bg="#222222")
        text_frame.pack(pady=20, padx=80, fill=tk.BOTH, expand=True)

        text_label = ttk.Label(
            text_frame, text=current_data["text"], style="Story.TLabel", wraplength=640, justify=tk.LEFT)
        text_label.pack(pady=10)

        self.choice_var = tk.StringVar(value="")
        self.choice_buttons = []
        for choice_text, choice_key in current_data["choices"]:
            btn = self.create_choice_button(
                self.content_frame, choice_text, choice_key)
            self.choice_buttons.append(btn)

        # Botão de Prosseguir
        continue_button = ttk.Button(self.content_frame, text="🚀 Prosseguir",
                                     command=self.process_choice,
                                     style="Action.TButton")
        continue_button.pack(pady=20)

        # Botão de Voltar (se não for a introdução)
        if len(self.current_choice_path) > 0:
            back_button = ttk.Button(self.content_frame, text="↩️ Voltar",
                                     command=self.go_back,
                                     style="Back.TButton")
            back_button.pack(pady=10)

        # Botão de Reiniciar
        restart_button = ttk.Button(self.content_frame, text="🔄 Reiniciar",
                                    command=self.restart_game,
                                    style="Action.TButton")
        restart_button.pack(pady=10)

    def get_current_story_segment(self):
        """
        Retorna o dicionário do segmento da história que deve ser exibido na tela atual,
        baseado em self.story_state e self.current_choice_path.
        """
        if self.story_state == "intro":
            return self.story["intro"]

        # Se estamos em um container de escolhas (não na intro e não no final_outcomes)
        # E se houver escolhas feitas no caminho
        if self.story_state in self.story and self.current_choice_path:
            current_container = self.story[self.story_state]
            # A chave do segmento a ser exibido é a última escolha feita.
            chosen_key = self.current_choice_path[-1]

            if chosen_key in current_container:
                return current_container[chosen_key]
            else:
                # Este else block é importante para depuração
                # Ele deve ser acionado se o self.story_state estiver correto
                # mas a chave da última escolha não corresponder a um segmento dentro dele.
                print(
                    f"DEBUG: KeyError in get_current_story_segment. story_state: {self.story_state}, chosen_key: {chosen_key}")
                print(
                    f"DEBUG: Content of self.story[self.story_state]: {current_container.keys()}")
                return None
        return None  # Estado da história ou caminho inválido

    def process_choice(self):
        """Processa a escolha atual e avança para a próxima parte da história."""
        selected_choice = self.choice_var.get()
        if not selected_choice:
            messagebox.showwarning(
                "Atenção", "Por favor, selecione uma opção antes de prosseguir.")
            return

        current_segment_data = self.get_current_story_segment()
        if not current_segment_data:
            messagebox.showerror(
                "Erro de Jogo", "Segmento da história atual não encontrado para processar escolha. Reiniciando.")
            self.restart_game()
            return

        # Adiciona a escolha selecionada ao caminho ANTES de determinar o próximo estado
        # Só adiciona se o selected_choice for de fato uma das escolhas válidas do segmento atual
        if any(choice_key == selected_choice for _, choice_key in current_segment_data.get("choices", [])):
            self.current_choice_path.append(selected_choice)
        else:
            messagebox.showerror(
                "Erro de Jogo", f"Escolha '{selected_choice}' não encontrada nas opções do segmento atual. Reiniciando.")
            self.restart_game()
            return

        # Determina o próximo story_state.
        # Se o segmento atual tem 'next_container_key', usamos ele.
        # Se o segmento atual tem 'attributes', significa que a escolha leva a um desfecho final.
        if "next_container_key" in current_segment_data:
            self.story_state = current_segment_data["next_container_key"]
        elif "attributes" in current_segment_data:  # Isso significa que o current_segment_data JÁ É um desfecho
            self.story_state = "final_outcomes"
        else:
            # Caso o segmento atual não aponte para um próximo container nem seja um desfecho
            messagebox.showerror(
                "Erro de Jogo", "Segmento de história mal definido (sem 'next_container_key' ou 'attributes'). Reiniciando.")
            self.current_choice_path.pop()  # Remove a escolha para evitar loop de erro
            self.restart_game()
            return

        self.show_story_screen()

    def go_back(self):
        """Volta para a tela anterior."""
        if not self.current_choice_path:
            messagebox.showinfo(
                "Informação", "Você já está na introdução do jogo.")
            return

        # Remove a última escolha do caminho para voltar ao estado anterior
        self.current_choice_path.pop()

        # Reseta os atributos para o estado inicial para que sejam recalculados ao refazer o caminho
        # (se a lógica de atributos for cumulativa e depender do caminho percorrido)
        self.player_attributes = {
            "Justice": 0,
            "Reputation": 0,
            "Empathy": 0,
            "Stress": 0
        }

        # Redefine o story_state para o ponto correto no caminho
        if not self.current_choice_path:
            self.story_state = "intro"
        else:
            # Precisa recalcular o story_state percorrendo o caminho até o penúltimo elemento
            temp_story_state_tracker = "intro"
            temp_current_segment = self.story["intro"]

            for choice_key in self.current_choice_path:
                if temp_story_state_tracker == "intro":
                    # Da intro, as escolhas levam para choices_lvl1
                    if "next_container_key" in temp_current_segment:
                        temp_story_state_tracker = temp_current_segment["next_container_key"]
                    else:
                        messagebox.showerror(
                            "Erro de Jogo", "Estrutura inconsistente ao voltar (intro sem next_container_key). Reiniciando.")
                        self.restart_game()
                        return

                # Agora, temp_story_state_tracker é o container (ex: "choices_lvl1", "choices_lvl2_1")
                # E temp_current_segment é o segmento específico DENTRO desse container.
                current_container_data = self.story.get(
                    temp_story_state_tracker)
                if not current_container_data or choice_key not in current_container_data:
                    messagebox.showerror(
                        "Erro de Jogo", f"Não foi possível retroceder. Chave '{choice_key}' não encontrada em '{temp_story_state_tracker}'. Reiniciando.")
                    self.restart_game()
                    return

                temp_current_segment = current_container_data[choice_key]

                if "next_container_key" in temp_current_segment:
                    temp_story_state_tracker = temp_current_segment["next_container_key"]
                elif "attributes" in temp_current_segment:
                    # Se chegamos a um desfecho, o próximo story_state seria "final_outcomes",
                    # mas para voltar, o story_state APONTA para o container do qual o desfecho veio.
                    # Ele já está no `temp_story_state_tracker` correto.
                    # Não muda o tracker, pois o desfecho final não leva a outro container de escolhas.
                    pass
                else:
                    messagebox.showerror(
                        "Erro de Jogo", "Estrutura inconsistente ao voltar (segmento sem next_container_key ou attributes). Reiniciando.")
                    self.restart_game()
                    return

            self.story_state = temp_story_state_tracker

        self.show_story_screen()

    def restart_game(self):
        """Reinicia o jogo para a introdução."""
        self.current_choice_path = []
        self.story_state = "intro"
        self.player_attributes = {  # Reseta os atributos também
            "Justice": 0,
            "Reputation": 0,
            "Empathy": 0,
            "Stress": 0
        }
        # Limpa o perfil salvo no user_data ao reiniciar o jogo
        if "profile" in self.user_data:
            del self.user_data["profile"]
        self.show_story_screen()

    def determine_player_profile(self):
        """
        Determina o perfil do jogador com base nos atributos finais.
        Perfis: "Aliado Silencioso", "Agente de Mudança", "Observador Neutro".
        """
        justice = self.player_attributes["Justice"]
        reputation = self.player_attributes["Reputation"]
        empathy = self.player_attributes["Empathy"]
        stress = self.player_attributes["Stress"]

        # Aliado Silencioso: Alta empatia, justiça moderada, reputação pode ser neutra/positiva, estresse moderado
        if empathy >= 7 and justice >= 5 and stress <= 8:
            return "Aliado Silencioso", "Você agiu com compaixão e buscou a justiça pelos meios menos ostensivos, construindo uma reputação de solidez e confiabilidade nos bastidores. Suas ações, embora discretas, tiveram um impacto significativo na vida de Elias e na reforma do sistema."

        # Agente de Mudança: Alta justiça, alta reputação (por vezes), alta empatia, pode ter estresse alto
        elif justice >= 8 and (reputation >= 7 or empathy >= 7) and stress <= 10:
            return "Agente de Mudança", "Você se tornou um catalisador para transformações profundas no sistema judiciário, não hesitando em confrontar a corrupção e promover a transparência. Suas escolhas, embora desafiadoras, resultaram em um impacto duradouro e positivo, mas com um custo pessoal de estresse."

        # Observador Neutro: Baixa empatia, justiça mais técnica, reputação neutra ou negativa, estresse pode ser variado
        else:  # Este será o perfil padrão se não se encaixar nos outros
            return "Observador Neutro", "Suas decisões foram predominantemente técnicas e focadas na aplicação da lei, por vezes ignorando as nuances humanas ou a pressão externa. Sua postura, embora imparcial, pode ter levado a desfechos questionáveis ou a uma percepção de frieza, resultando em estresse variável."

   

   

    def show_final_outcome(self):
        self.clear_content_frame()
        final_key = self.current_choice_path[-1] if self.current_choice_path else None

        if final_key and final_key in self.story.get("final_outcomes", {}):
            outcome = self.story["final_outcomes"][final_key]
        else:
            messagebox.showerror(
                "Erro de Desfecho", "Desfecho final não encontrado. Reiniciando o jogo.")
            self.restart_game()
            return

        # Aplica os atributos ao jogador
        for attr, value in outcome.get("attributes", {}).items():
            if attr in self.player_attributes:
                self.player_attributes[attr] += value

        # Container principal sem rolagem
        main_frame = tk.Frame(self.content_frame, bg="#222222")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Primeira parte: Resultado
        result_frame = tk.Frame(main_frame, bg="#222222", padx=20, pady=10)
        result_frame.pack(fill=tk.X, pady=(0, 20))

        # Título do resultado
        title_label = ttk.Label(
            result_frame, 
            text=outcome["title"], 
            style="TLabel",
            font=("Helvetica", 18, "bold"),
            foreground="#FFD700"
        )
        title_label.pack(pady=(10, 20))

        # Texto do resultado
        text_frame = tk.Frame(
            result_frame, 
            bg="#333333", 
            padx=15, 
            pady=15,
            relief="groove",
            borderwidth=2
        )
        text_frame.pack(fill=tk.BOTH, padx=10, pady=5)

        text_label = ttk.Label(
            text_frame, 
            text=outcome["text"], 
            style="Story.TLabel", 
            wraplength=700, 
            justify=tk.LEFT,
            font=("Helvetica", 12)
        )
        text_label.pack()

        # Seção de informações sobre prisões injustas
        prison_frame = tk.Frame(main_frame, bg="#222222", padx=20, pady=10)
        prison_frame.pack(fill=tk.X, pady=(20, 10))

        # Título da seção
        prison_title = ttk.Label(
            prison_frame,
            text="Prisões Injustas no Brasil",
            style="TLabel",
            font=("Helvetica", 16, "bold"),
            foreground="#FF6347"
        )
        prison_title.pack(pady=(0, 15))

        # Container para o texto
        prison_text_frame = tk.Frame(
            prison_frame,
            bg="#2a2a2a",
            padx=20,
            pady=15,
            relief="ridge",
            borderwidth=1
        )
        prison_text_frame.pack(fill=tk.BOTH, padx=10)

        prison_text = """Prisões Injustas no Brasil: o peso de uma decisão
No Brasil, centenas de pessoas são privadas de liberdade de forma indevida todos os anos. Uma das principais causas dessas prisões é a fragilidade das provas, como reconhecimentos fotográficos imprecisos ou testemunhos sem respaldo técnico. Entre 2012 e 2020, foram registradas ao menos 90 prisões injustas por reconhecimento fotográfico — sendo 73 apenas no estado do Rio de Janeiro, com predominância de vítimas negras e jovens.

A desigualdade racial e social, somada à pressa em resolver crimes, cria um terreno fértil para erros judiciais que custam a vida de inocentes. Em 2009, o então presidente do STF, ministro Gilmar Mendes, alertou que cerca de 20% das pessoas presas no país estavam em situação ilegal, seja por erros processuais ou ausência de provas sólidas.

Diante dessa realidade, iniciativas como o Innocence Project Brasil lutam para reverter condenações injustas e promover debates sobre as falhas estruturais do sistema. """
        
        prison_label = ttk.Label(
            prison_text_frame, 
            text=prison_text, 
            style="Story.TLabel", 
            wraplength=700, 
            justify=tk.LEFT,
            font=("Helvetica", 11)
        )
        prison_label.pack()

        # Botão para continuar (embaixo de tudo)
        button_container = tk.Frame(main_frame, bg="#222222", pady=20)
        button_container.pack(fill=tk.X)

        continue_button = ttk.Button(
            button_container, 
            text="Continuar para Reflexão →",
            command=lambda: self.show_reflection_screen(outcome),
            style="Action.TButton"
        )
        continue_button.pack(pady=10, ipadx=20, ipady=5)

    def show_reflection_screen(self, outcome):
        """Mostra a tela de reflexão sem barra de rolagem."""
        self.clear_content_frame()

        # Container principal
        main_frame = tk.Frame(self.content_frame, bg="#222222")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Título da reflexão
        title_frame = tk.Frame(main_frame, bg="#222222", padx=20, pady=20)
        title_frame.pack(fill=tk.X)

        title_label = ttk.Label(
            title_frame,
            text="Reflexão sobre sua Decisão",
            style="TLabel",
            font=("Helvetica", 18, "bold"),
            foreground="#FFD700"
        )
        title_label.pack()

        # Texto de reflexão
        reflection_frame = tk.Frame(
            main_frame,
            bg="#333333",
            padx=25,
            pady=20,
            relief="groove",
            borderwidth=2
        )
        reflection_frame.pack(fill=tk.BOTH, padx=30, pady=10)

        reflection_text = """E agora… repense sua decisão no caso de Elias
Você acaba de viver a história de Elias, um jovem negro acusado de um crime grave com base no relato de uma única testemunha que afirma tê-lo visto no local do crime. Durante o julgamento, você – no papel de juiz – teve que decidir se havia elementos suficientes para condená-lo ou se a dúvida deveria pesar a favor da liberdade.

O caso de Elias não é ficção isolada. Ele representa os muitos brasileiros que enfrentam a Justiça sem provas concretas, apenas com o peso do preconceito e da palavra de terceiros.

Agora que conhece os dados, os contextos e as consequências reais de decisões precipitadas, reflita:

🔍 Será que você julgou com base em evidências sólidas ou em suposições?
⚖️ Quantos Elias estão hoje atrás das grades por decisões semelhantes à que você tomou?
🧠 Se fosse com alguém que você ama… qual justiça você esperaria?

Na Pele e na Consciência não entrega respostas prontas. Ele te entrega a pergunta:
👉 Você faria diferente agora que sabe a verdade?"""

        text_label = ttk.Label(
            reflection_frame, 
            text=reflection_text, 
            style="Story.TLabel", 
            wraplength=700, 
            justify=tk.LEFT,
            font=("Helvetica", 12)
        )
        text_label.pack()

        # Botão para ver atributos (embaixo de tudo)
        button_container = tk.Frame(main_frame, bg="#222222", pady=20)
        button_container.pack(fill=tk.X)

        profile_button = ttk.Button(
            button_container, 
            text="Ver Meu Perfil e Atributos →",
            command=lambda: self.show_final_profile(outcome),
            style="Action.TButton"
        )
        profile_button.pack(pady=10, ipadx=20, ipady=5)

    def show_final_profile(self, outcome):
        """Mostra os atributos finais sem barra de rolagem."""
        self.clear_content_frame()

        # Determinar e exibir o perfil personalizado
        profile_name, profile_description = self.determine_player_profile()
        
        # Container principal
        main_frame = tk.Frame(self.content_frame, bg="#222222")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Título principal
        title_frame = tk.Frame(main_frame, bg="#222222", padx=20, pady=20)
        title_frame.pack(fill=tk.X)

        title_label = ttk.Label(
            title_frame, 
            text="Seu Desempenho no Julgamento", 
            style="TLabel", 
            font=("Helvetica", 18, "bold"),
            foreground="#FFD700"
        )
        title_label.pack()

        # Seção de atributos
        attributes_frame = tk.Frame(main_frame, bg="#333333", padx=20, pady=20)
        attributes_frame.pack(fill=tk.X, padx=30, pady=10)

        ttk.Label(
            attributes_frame, 
            text="Atributos Finais:", 
            style="Attribute.TLabel", 
            font=("Helvetica", 14, "bold"),
            foreground="#FFFFFF"
        ).pack(pady=(0, 15))

        # Traduzindo os nomes dos atributos
        attr_translation = {
            "Justice": "Justiça",
            "Reputation": "Reputação",
            "Empathy": "Empatia",
            "Stress": "Estresse"
        }

        # Criando um frame para organizar os atributos em uma grade
        attr_grid = tk.Frame(attributes_frame, bg="#333333")
        attr_grid.pack()

        for i, (attr, value) in enumerate(self.player_attributes.items()):
            # Frame para cada atributo (cartão)
            attr_frame = tk.Frame(
                attr_grid, 
                bg="#444444", 
                relief="ridge", 
                bd=2, 
                padx=15, 
                pady=15,
                highlightbackground="#555555",
                highlightthickness=1
            )
            attr_frame.grid(row=i//2, column=i%2, padx=15, pady=15, sticky="nsew")

            # Nome do atributo traduzido
            ttk.Label(
                attr_frame, 
                text=attr_translation.get(attr, attr), 
                style="Attribute.TLabel", 
                font=("Helvetica", 12, "bold"),
                foreground="#FFFFFF"
            ).pack()

            # Valor numérico
            ttk.Label(
                attr_frame, 
                text=f"{value:+d}",
                font=("Helvetica", 14, "bold"),
                foreground="#FFD700" if value >= 0 else "#FF6347"
            ).pack(pady=(5, 10))

            # Barra de progresso visual melhorada
            canvas = tk.Canvas(
                attr_frame, 
                width=220, 
                height=25, 
                bg="#444444", 
                highlightthickness=0
            )
            canvas.pack()
            
            # Calcula a largura da barra
            max_value = 20
            bar_width = min(abs(value) * (220/max_value), 220)
            fill_color = "#4CAF50" if value >= 0 else "#F44336"
            
            # Desenha a barra de fundo cinza
            canvas.create_rectangle(0, 0, 220, 25, fill="#555555", outline="")
            # Desenha a barra de valor
            if value >= 0:
                canvas.create_rectangle(0, 0, bar_width, 25, fill=fill_color, outline="")
            else:
                canvas.create_rectangle(220-bar_width, 0, 220, 25, fill=fill_color, outline="")
            
            # Texto do valor no meio
            canvas.create_text(
                110, 
                13, 
                text=f"{value:+d}", 
                fill="white", 
                font=("Helvetica", 10, "bold")
            )

        # Seção de perfil personalizado
        profile_frame = tk.Frame(
            main_frame, 
            bg="#333333", 
            padx=25, 
            pady=25,
            relief="groove", 
            borderwidth=2
        )
        profile_frame.pack(fill=tk.BOTH, padx=30, pady=20)

        ttk.Label(
            profile_frame, 
            text=f"Seu Perfil: {profile_name}", 
            style="Attribute.TLabel", 
            font=("Helvetica", 16, "bold"),
            foreground="#FFD700"
        ).pack(pady=(0, 15))

        # Texto de descrição
        desc_frame = tk.Frame(profile_frame, bg="#3a3a3a", padx=15, pady=15)
        desc_frame.pack(fill=tk.BOTH)

        ttk.Label(
            desc_frame, 
            text=profile_description,
            style="Attribute.TLabel", 
            wraplength=600, 
            justify=tk.CENTER,
            font=("Helvetica", 12),
            foreground="#E0E0E0"
        ).pack()

        # Salvar o perfil no user_data para que o menu possa acessá-lo
        self.user_data["profile"] = {
            "name": profile_name, "description": profile_description}

        # Botões na parte inferior
        button_container = tk.Frame(main_frame, bg="#222222", pady=5)
        button_container.pack(fill=tk.X)

        # Frame para organizar os botões
        buttons_frame = tk.Frame(button_container, bg="#222222")
        buttons_frame.pack()

        # Botão de Reiniciar
        restart_button = ttk.Button(
            buttons_frame, 
            text="🔄 Reiniciar Jogo",
            command=self.restart_game,
            style="Secondary.TButton"
        )
        restart_button.pack(side=tk.LEFT, padx=15, ipadx=15, ipady=5)

        # Botão de Sair
        exit_button = ttk.Button(
            buttons_frame, 
            text="🚪 Sair para o Menu",
            command=self.exit_to_menu,
            style="Secondary.TButton"
        )
        exit_button.pack(side=tk.LEFT, padx=15, ipadx=15, ipady=5)



    def exit_to_menu(self):
        """Volta para o menu principal e mostra a seção de perfil personalizado"""
        self.clear_content_frame()
        self.menu_app.show_perfil_personalizado()  # Mostra a seção de perfil no menu



