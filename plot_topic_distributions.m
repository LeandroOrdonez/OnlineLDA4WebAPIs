function plot_topic_distributions()
    gamma=load('parameters/gamma-all.dat');
    indices = round((rand(1,20).*814)+1);
    figure
    for i = 1:20
        subplot(4,5,i)
        plot(gamma(indices(i),:)./sum(gamma(indices(i),:)))
        title(cstrcat("Operation ", num2str(indices(i))))
    end
endfunction
