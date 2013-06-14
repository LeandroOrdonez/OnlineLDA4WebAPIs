function plot_topic_distributions()
    gamma=load('parameters/gamma-all.dat');
    figure
    for i = 1:40
        subplot(5,8,i)
        plot(gamma(i,:)./sum(gamma(i,:)))
        title(cstrcat("Operation ", num2str(i)))
    end
endfunction
