import seaborn as sns


def encode_depto_pretty(series):
    "Codifica departamento INE, formateado"
    deptos_dict = {
        'Montevideo': 1,
        'Artigas': 2,
        'Canelones': 3,
        'Cerro Largo': 4,
        'Colonia': 5,
        'Durazno': 6,
        'Flores': 7,
        'Florida': 8,
        'Lavalleja': 9,
        'Maldonado': 10,
        'Paysandú': 11,
        'Río Negro': 12,
        'Rivera': 13,
        'Rocha': 14,
        'Salto': 15,
        'San José': 16,
        'Soriano': 17,
        'Tacuarembó': 18,
        'Treinta y Tres': 19
        }
    cod = series.map(deptos_dict).values

    return cod[0]


nom_depto = [
    'Montevideo',
    'Artigas',
    'Canelones',
    'Cerro Largo',
    'Colonia', 
    'Durazno',
    'Flores',
    'Florida',
    'Lavalleja',
    'Maldonado',
    'Paysandú',
    'Río Negro',
    'Rivera',
    'Rocha',
    'Salto',
    'San José',
    'Soriano',
    'Tacuarembó',
    'Treinta y Tres'
    ]


def bars_pyramid(df, axis, col_agrup, colors, bar_order):
    "Grafica barras para pirámdes"
    for c, group in zip(colors, df[col_agrup].unique()):
        sns.barplot(x='porc_pers',
                    y='tramo',
                    data=df.loc[df[col_agrup]==group, :],
                    order = bar_order,
                    color=c,
                    ax=axis)


def etiquetar_sexos(x_position, y_position, ax_name, colors, font_size):
    # Varones
    ax_name.text(x_position*-1, y_position, 'Varones',
    horizontalalignment='left',
    color=colors[0], fontsize=font_size)
    # Mujeres
    ax_name.text(x_position, y_position, 'Mujeres',
    horizontalalignment='right',
    color=colors[1], fontsize=font_size)


y_labels = [
    '+95',
    '90-94',
    '85-89',
    '80-84',
    '75-79',
    '70-74',
    '65-69',
    '60-64',
    '55-59',
    '50-54',
    '45-49',
    '40-44',
    '35-39',
    '30-34',
    '25-29',
    '20-24',
    '15-19',
    '10-14',
    '5-9',
    '0-4'
    ]