from django.db import models
from django.contrib.auth.models import User  # Importa o modelo de usuário padrão do Django
from .relationship import Relationship  # Importa o modelo Relationship do mesmo pacote
from django.core.exceptions import ValidationError  # Importa ValidationError para validação personalizada
import hashlib  # Importa hashlib para gerar hash MD5

def validate_image(image):
    """
    Valida o tamanho da imagem para garantir que não exceda o limite permitido.
    """
    try:
        file_size = image.size  # Obtém o tamanho do arquivo de imagem
        limit_kb = 500  # Define o limite de tamanho da imagem em KB
        if file_size > limit_kb * 1024:
            # Lança um erro de validação se o tamanho da imagem exceder o limite
            raise ValidationError(f"O tamanho máximo do arquivo é {limit_kb}KB")
    except FileNotFoundError:
        # Lança um erro de validação se o arquivo de imagem não for encontrado
        raise ValidationError("O arquivo de imagem não foi encontrado.")

class Profile(models.Model):
    """
    Modelo de perfil do usuário, estendendo o modelo User padrão do Django.
    """
    id = models.BigAutoField(primary_key=True)  # Campo ID com auto incremento, usado como chave primária
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Relacionamento um-para-um com o modelo User
    bio = models.CharField(default="Ola, Sou novo aqui!", max_length=100)  # Campo de texto para a biografia do usuário
    image = models.ImageField(default="default.png", validators=[validate_image])  # Campo de imagem com validação personalizada

    def __str__(self):
        # Retorna uma representação em string do perfil, mostrando o nome de usuário
        return f"Perfil de {self.user.username}"

    def following(self):
        """
        Retorna os usuários que o usuário atual está seguindo.
        """
        # Obtém os IDs dos usuários que o usuário atual está seguindo
        user_ids = Relationship.objects.filter(from_user=self.user).values_list(
            "to_user_id", flat=True
        )
        # Retorna os usuários correspondentes aos IDs obtidos
        return User.objects.filter(id__in=user_ids)

    def followers(self):
        """
        Retorna os seguidores do usuário atual.
        """
        # Obtém os IDs dos usuários que estão seguindo o usuário atual
        user_ids = Relationship.objects.filter(to_user=self.user).values_list(
            "from_user_id", flat=True
        )
        # Retorna os usuários correspondentes aos IDs obtidos
        return User.objects.filter(id__in=user_ids)

    def followers_count(self):
        """
        Retorna o número de seguidores do usuário atual.
        """
        return self.followers().count()

    def following_count(self):
        """
        Retorna o número de usuários que o usuário atual está seguindo.
        """
        return self.following().count()


    @property
    def image_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url
        return 'https://cdn-icons-png.flaticon.com/512/709/709722.pn'