#This side UP
Aplicativo para a análise da respiração baseado em sensores de aceleração

refereências:
https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3203837/
https://www.researchgate.net/publication/224317741_Estimation_of_respiratory_waveform_using_an_accelerometer

To do:
-1: Aquisitar o sensor;
  -celeular;(feito)
  -acelerometro;
-2: adaptação temporal;

-3: filtragem inicial;
-4: DSP;
-5: Respostas;

Descrição do DSP:
-Detectar o vetor Ĝ;
-Subtrair o nivel Continúo do sinal;
-Verificar se a energia do sinal tende a zero;
-Detectar se existe algum sinal periódico na faixa de banda da respiração;
-Inicia a detecção da janela deslizante de análise;
