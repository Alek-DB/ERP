import sys
from PySide6.QtWidgets import  QLabel, QWidget, QHBoxLayout, QScrollArea, QVBoxLayout , QGroupBox



class QListe(QWidget):
    def __init__(self, title, objects, section_names):
        super().__init__()

        v_outer_layout = QVBoxLayout()
        v_outer_layout.addWidget(QLabel(title))

        # Créer un QScrollArea
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)  # Permet à l'intérieur de s'ajuster

        # Créer un widget pour contenir les objets et le mettre dans la ScrollArea
        scroll_content = QWidget()
        v_inner_layout = QVBoxLayout(scroll_content)

        names_layout = QHBoxLayout()
        for name in section_names:
            label = QLabel(name)
            label.setWordWrap(True)
            label.setFixedWidth(100)
            names_layout.addWidget(label)
            names_layout.addStretch()
        v_inner_layout.addLayout(names_layout)

        # Si objects est unidimensionnel, ajoutez des widgets, sinon créez un layout pour chaque ligne
        for obj in objects:
            if not self._is_two_dimensional(objects):
                obj.setFixedWidth(100)
                obj.setMinimumHeight(20)
                obj.setWordWrap(True)
                v_inner_layout.addWidget(obj)
                v_inner_layout.addStretch()
            else:
                hlayout = QHBoxLayout()
                for o in obj:
                    o.setFixedWidth(100)
                    o.setMinimumHeight(20)
                    o.setWordWrap(True)
                    hlayout.addWidget(o)
                    hlayout.addStretch()
                v_inner_layout.addLayout(hlayout)

        v_inner_layout.addStretch()

        scroll_area.setWidget(scroll_content)

        group_box = QGroupBox()
        group_box.setMinimumWidth(300)
        group_box.setFixedHeight(300)

        group_box_layout = QVBoxLayout(group_box)
        group_box_layout.addWidget(scroll_area)

        v_outer_layout.addWidget(group_box)
        v_outer_layout.addStretch()

        self.setLayout(v_outer_layout)

    def _is_two_dimensional(self, tableau):
        # Vérifie si le tableau est une liste
        if not isinstance(tableau, list):
            return False

        # Vérifie si chaque élément est une liste
        if not all(isinstance(ligne, list) for ligne in tableau):
            return False

        # Vérifie que toutes les sous-listes ont la même longueur
        longueur = len(tableau[0])
        if not all(len(ligne) == longueur for ligne in tableau):
            return False

        return True

 
