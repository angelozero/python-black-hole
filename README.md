# Simulando a Luz em torno do Buraco Negro em Python

Uma simulação física em Python que utiliza a **Métrica de Schwarzschild** para demonstrar como a luz (fótons) se comporta ao passar perto de um buraco negro estático. O projeto visualiza fenômenos como a **Lente Gravitacional** e a **Esfera de Fótons**.

![Simulação do Buraco Negro](blackhole_simulation.gif)

---

Este script resolve as equações geodésicas da Relatividade Geral para traçar a trajetória da luz no espaço-tempo curvo. 

### O que você verá na animação:
* **Raios Azuis:** Fótons que sofrem deflexão gravitacional, mas conseguem escapar para o infinito.
* **Raios Laranjas:** Fótons que cruzam o horizonte de eventos e são capturados pelo buraco negro.
* **Linha Tracejada Vermelha:** A **Esfera de Fótons** ($1.5 \times R_s$), a região onde a gravidade é tão intensa que a luz pode orbitar o buraco negro.
* **Círculo Preto Central:** O **Horizonte de Eventos** ($R_s$), o ponto de não retorno.




## 📖 A Física por trás

A trajetória da luz é calculada usando a variável $u = 1/r$ em função do ângulo $\phi$, seguindo a equação derivada da relatividade geral:

![alt text](image.png)

Para simplificação computacional, o código utiliza unidades naturalizadas onde $G = c = 1$.

No código, essa derivada é implementada na função `deriv`, onde transformamos uma equação de segunda ordem em um sistema de duas equações de primeira ordem para o integrador `odeint`:

```python
def deriv(u_phi, phi, rs):
    u, p = u_phi
    # du/dphi = p
    # dp/dphi = 1.5 * rs * u^2 - u
    return [p, 1.5 * rs * u**2 - u]
```

#### 2. O Parâmetro de Impacto ($b$)
O destino da luz depende de quão perto ela tenta passar do centro, uma distância perpendicular chamada **parâmetro de impacto**. No código, definimos a velocidade inicial ($p_0$) com base nesse valor:

```python
# p0 define a direção inicial do raio baseado na distância 'b'
p0 = -np.sqrt(np.abs(1.0/b**2 - (1.0 - rs/distancia_ini) * u0**2))
```

#### 3. Pontos Críticos
A simulação destaca duas regiões fundamentais que definem a anatomia de um buraco negro:

* **Horizonte de Eventos ($R_s$):** A fronteira de onde nada escapa. No código, representado pelo círculo preto sólido.
* **Esfera de Fótons ($1.5 R_s$):** A última órbita circular estável para a luz. Raios que chegam mais perto que isso (em laranja no gráfico) são inevitavelmente sugados.

```python
# Definindo as regiões críticas no gráfico
bh = plt.Circle((0, 0), rs, color='black') # Horizonte de Eventos
photon_sphere = plt.Circle((0, 0), 1.5*rs, ls='--') # Esfera de Fótons
```