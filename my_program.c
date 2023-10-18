#include <stdio.h>

int main(int argc, char *argv[])
{
	(void)argc;

	char **arg = argv;

	while (*arg != NULL)
	{
		printf("%s\n", *arg);
		arg++;
	}
	return 0;
}
