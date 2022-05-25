#���ؿ������t�ֲ�
#nΪ���ɶȣ�numΪ���ؿ������
mt=function(n,num){
  x=rnorm(num)
  y=0
  for(i in 1:n){
    y=y+rnorm(num)^2
  }
  return(x/(y/n)^0.5)
}
#���ؿ���������
#qΪ��λ����nΪ���ɶȣ�numΪ���ؿ������
mpt=function(q,n,num){
  z=mt(n,num)
  return(length(z[z<q])/num)
}
#���ؿ�������λ��
#pΪ���ʣ�nΪ���ɶȣ�numΪ���ؿ������
mqt=function(p,n,num){
  z=mt(n,num)
  return(z[order(z)][round(p*num)])
}
k=1000
list=NULL
h=100
for(i in 1:h){
  list[i]=mqt(0.5,5,k)
}
y=0
for(i in 1:h){
  y=y+(list[i]-0)^2
}
mean(list)
y
variance=log(c(1.849496,0.1686753,0.01729059,0.001307301,0.0001492519),10)
x=factor(c('100','1000','10000','1e+05','1e+06'))
data=data.frame(variance,x)
library(ggplot2)

ggplot(data=data,aes(x,variance))+geom_point()+labs(x="k", y="Var(log10)")+
  theme(panel.grid=element_blank(), panel.background=element_rect(fill='transparent', color='black'))

n=5
#t�ֲ������ܶȹ�ʽ
ft=function(x,n){
  return(gamma((n+1)/2)/(n*pi)^0.5/gamma(n/2)*(1+(x^2/n))^(-(n+1)/2))
}
#�������
fpt=function(q,n){
  p=as.numeric(integrate(ft,lower=-Inf,upper=q,100)[1])
  return(p)
}
#�����λ��
fqt=function(p,n){
  q=0
  while(1){
    d=(fpt(q,n)-p)/ft(q,n)
    q=q-d
    if(abs(d)<1e-6){
      break
    }
  }
  return(q)
}



