#!/usr/bin/env python3
"""
Инженерный калькулятор единиц и физических параметров гидравлики (Hydraulics Calculator)
Кафедра ИСИТ / РГУ нефти и газа им. И.М. Губкина.

Поддерживает:
1. Перевод несистемных единиц в систему СИ (расход, давление, вязкость, диаметр, длина).
2. Расчет плотности по давлению и температуре: rho(T, p).
3. Расчет гидродинамики трубы: скорость, Reynolds (Re), зоны сопротивления, lambda (Альтшуль, Блазиус, Шифринсон).
4. Расчет потерь напора (Дарси-Вейсбах), гидравлического уклона i, модуля сопротивления s.
5. Расчет гидроудара по Жуковскому: скорость волны c, фаза tau, скачок давления delta_p.
"""

import sys
import math
import argparse

GRAVITY = 9.80665
ATM_PRESSURE = 101325.0

# ---------------------------------------------------------
# Конвертер единиц измерения
# ---------------------------------------------------------
class UnitConverter:
    @staticmethod
    def mass_flow_to_si(val: float, unit: str) -> float:
        """Перевод массового расхода в кг/с"""
        u = unit.lower().strip()
        if u in ['kg/s', 'кг/с']:
            return val
        elif u in ['t/h', 'т/ч']:
            return val * 1000.0 / 3600.0
        elif u in ['t/day', 'т/сут', 'т/сутки']:
            return val * 1000.0 / 86400.0
        elif u in ['g/s', 'г/с']:
            return val * 1e-3
        raise ValueError(f"Неизвестная единица массового расхода: {unit}")

    @staticmethod
    def volume_flow_to_si(val: float, unit: str) -> float:
        """Перевод объемного расхода в м3/с"""
        u = unit.lower().strip()
        if u in ['m3/s', 'м3/с', 'м^3/с']:
            return val
        elif u in ['m3/h', 'м3/ч', 'м^3/ч']:
            return val / 3600.0
        elif u in ['m3/day', 'м3/сут', 'м3/сутки']:
            return val / 86400.0
        elif u in ['l/s', 'л/с']:
            return val * 1e-3
        elif u in ['l/min', 'л/мин']:
            return val * 1e-3 / 60.0
        raise ValueError(f"Неизвестная единица объемного расхода: {unit}")

    @staticmethod
    def pressure_to_si(val: float, unit: str) -> float:
        """Перевод давления в Паскали (Па)"""
        u = unit.lower().strip()
        if u in ['pa', 'па']:
            return val
        elif u in ['kpa', 'кпа']:
            return val * 1e3
        elif u in ['mpa', 'мпа']:
            return val * 1e6
        elif u in ['bar', 'бар']:
            return val * 1e5
        elif u in ['atm', 'атм']:
            return val * 101325.0
        elif u in ['at', 'ат']:
            return val * 98066.5
        elif u in ['mmhg', 'мм рт.ст.', 'мм рт ст']:
            return val * 133.322
        elif u in ['m w.c.', 'м вод.ст.', 'м вод ст']:
            return val * GRAVITY * 1000.0
        raise ValueError(f"Неизвестная единица давления: {unit}")

    @staticmethod
    def viscosity_kinematic_to_si(val: float, unit: str) -> float:
        """Перевод кинематической вязкости в м2/с"""
        u = unit.lower().strip()
        if u in ['m2/s', 'м2/с', 'м^2/с']:
            return val
        elif u in ['cst', 'сст', 'mm2/s', 'мм2/с', 'мм^2/с']:
            return val * 1e-6
        elif u in ['st', 'ст']:
            return val * 1e-4
        raise ValueError(f"Неизвестная единица кинематической вязкости: {unit}")

    @staticmethod
    def length_to_si(val: float, unit: str) -> float:
        """Перевод длины/диаметра в метры (м)"""
        u = unit.lower().strip()
        if u in ['m', 'м']:
            return val
        elif u in ['km', 'км']:
            return val * 1000.0
        elif u in ['mm', 'мм']:
            return val * 1e-3
        elif u in ['cm', 'см']:
            return val * 1e-2
        raise ValueError(f"Неизвестная единица длины: {unit}")


# ---------------------------------------------------------
# Физические свойства нефтей и сред
# ---------------------------------------------------------
class FluidProperties:
    @staticmethod
    def calc_density(rho20: float, temperature_c: float, pressure_pa: float = ATM_PRESSURE,
                     xi: float = 0.0008, bulk_modulus: float = 1.5e9) -> float:
        """
        Расчет плотности капельной жидкости по температуре и давлению (Лурье, 2003, 2012):
        rho(p, T) = rho20 * [1 + xi * (20 - T) + (p - p_atm) / K]
        """
        term_temp = xi * (20.0 - temperature_c)
        term_press = (pressure_pa - ATM_PRESSURE) / bulk_modulus
        return rho20 * (1.0 + term_temp + term_press)


# ---------------------------------------------------------
# Гидродинамические расчеты течений в трубах
# ---------------------------------------------------------
class PipelineHydraulics:
    @staticmethod
    def calc_velocity(flow_rate_m3_s: float, diameter_m: float) -> float:
        """Средняя скорость потока в круглой трубе v = 4*Q / (pi * d^2)"""
        area = (math.pi * diameter_m**2) / 4.0
        return flow_rate_m3_s / area

    @staticmethod
    def calc_reynolds(velocity_m_s: float, diameter_m: float, kinematic_viscosity_m2_s: float) -> float:
        """Число Рейнольдса Re = |v| * d / nu"""
        return abs(velocity_m_s) * diameter_m / kinematic_viscosity_m2_s

    @staticmethod
    def determine_regime_and_friction_factor(reynolds: float, diameter_m: float, roughness_m: float) -> tuple[str, float]:
        """
        Определение зоны гидравлического сопротивления и расчет коэффициента трения lambda.
        Возвращает: (название зоны, lambda).
        """
        if reynolds < 1e-9:
            return "Покой (нулевой расход)", 0.0

        rel_roughness = roughness_m / diameter_m

        if reynolds < 2320.0:
            # Ламинарный режим (Пуазейль)
            return "Ламинарный режим (Пуазейль)", 64.0 / reynolds

        re_smooth_limit = 10.0 / rel_roughness if rel_roughness > 0 else 1e9
        re_rough_limit = 500.0 / rel_roughness if rel_roughness > 0 else 1e9

        if reynolds < re_smooth_limit and reynolds < 1e5:
            # Зона гидравлически гладких труб (Блазиус)
            lam = 0.3164 / (reynolds**0.25)
            return "Гидравлически гладкие трубы (Блазиус)", lam
        elif reynolds <= re_rough_limit:
            # Зона смешанной шероховатости / доквадратичная (Альтшуль)
            lam = 0.11 * ((rel_roughness + 68.0 / reynolds)**0.25)
            return "Зона смешанного трения (Альтшуль)", lam
        else:
            # Квадратичная область шероховатых труб (Шифринсон)
            lam = 0.11 * (rel_roughness**0.25)
            return "Квадратичная область (Шифринсон)", lam

    @staticmethod
    def calc_pipe_losses(flow_rate_m3_s: float, length_m: float, diameter_m: float,
                         roughness_m: float, kinematic_viscosity_m2_s: float,
                         density_kg_m3: float) -> dict:
        """Комплексный расчет потерь на участке трубы"""
        vel = PipelineHydraulics.calc_velocity(flow_rate_m3_s, diameter_m)
        re = PipelineHydraulics.calc_reynolds(vel, diameter_m, kinematic_viscosity_m2_s)
        regime, lam = PipelineHydraulics.determine_regime_and_friction_factor(re, diameter_m, roughness_m)

        # Потери напора по Дарси-Вейсбаху [м]
        if abs(vel) < 1e-9:
            head_loss = 0.0
        else:
            head_loss = lam * (length_m / diameter_m) * (vel * abs(vel)) / (2.0 * GRAVITY)

        hydraulic_gradient = head_loss / length_m if length_m > 0 else 0.0
        pressure_drop = density_kg_m3 * GRAVITY * head_loss
        
        # Модуль гидравлического сопротивления s [с2/м5]
        s_modulus = (8.0 * lam * length_m) / (math.pi**2 * GRAVITY * diameter_m**5) if diameter_m > 0 else 0.0

        return {
            "velocity": vel,
            "reynolds": re,
            "regime": regime,
            "friction_factor": lam,
            "head_loss_m": head_loss,
            "hydraulic_gradient": hydraulic_gradient,
            "pressure_drop_pa": pressure_drop,
            "pressure_drop_mpa": pressure_drop / 1e6,
            "resistance_modulus_s": s_modulus
        }

    @staticmethod
    def calc_water_hammer(density_kg_m3: float, diameter_m: float, wall_thickness_m: float,
                          length_m: float, delta_v_m_s: float,
                          bulk_modulus: float = 1.5e9, young_modulus: float = 2.06e11) -> dict:
        """
        Расчет параметров гидравлического удара по формуле Жуковского — Кортевега:
        c = sqrt((K/rho) / (1 + (K/E)*(D/e)))
        """
        denom = 1.0 + (bulk_modulus / young_modulus) * (diameter_m / wall_thickness_m)
        c_wave = math.sqrt((bulk_modulus / density_kg_m3) / denom)

        phase_tau = 2.0 * length_m / c_wave
        delta_p_direct = density_kg_m3 * c_wave * abs(delta_v_m_s)
        delta_h_direct = c_wave * abs(delta_v_m_s) / GRAVITY

        return {
            "wave_speed_c": c_wave,
            "phase_tau_s": phase_tau,
            "delta_p_joukowsky_pa": delta_p_direct,
            "delta_p_joukowsky_mpa": delta_p_direct / 1e6,
            "delta_h_joukowsky_m": delta_h_direct
        }


def print_banner():
    print("=" * 70)
    print("  Инженерный калькулятор гидравлики (Hydraulics Calculator CLI)")
    print("  Кафедра ИСИТ / РГУ нефти и газа им. И.М. Губкина")
    print("=" * 70)


def interactive_mode():
    print_banner()
    print("\nВыберите режим работы:")
    print("  1. Перевод единиц измерения в СИ")
    print("  2. Расчет плотности по давлению и температуре rho(T, p)")
    print("  3. Комплексный расчет участка трубы (Re, режим, lambda, потери)")
    print("  4. Расчет прямого гидроудара по Жуковскому")
    print("  0. Выход\n")

    choice = input("Введите номер пункта [1-4]: ").strip()
    if choice == '1':
        print("\n--- Перевод единиц измерения ---")
        val = float(input("Числовое значение: "))
        unit = input("Единица измерения (т/ч, м3/ч, МПа, бар, сСт, мм, км): ").strip()
        try:
            if unit.lower() in ['т/ч', 't/h', 'кг/с', 'kg/s', 'т/сут']:
                res = UnitConverter.mass_flow_to_si(val, unit)
                print(f"Результат в СИ: {res:.8f} кг/с")
            elif unit.lower() in ['м3/ч', 'm3/h', 'м3/с', 'm3/s', 'л/с', 'l/s']:
                res = UnitConverter.volume_flow_to_si(val, unit)
                print(f"Результат в СИ: {res:.8f} м3/с")
            elif unit.lower() in ['мпа', 'mpa', 'бар', 'bar', 'атм', 'atm', 'кпа']:
                res = UnitConverter.pressure_to_si(val, unit)
                print(f"Результат в СИ: {res:.2f} Па ({res/1e6:.6f} МПа)")
            elif unit.lower() in ['сст', 'cst', 'мм2/с', 'м2/с', 'ст']:
                res = UnitConverter.viscosity_kinematic_to_si(val, unit)
                print(f"Результат в СИ: {res:.8e} м2/с")
            elif unit.lower() in ['мм', 'mm', 'км', 'km', 'см']:
                res = UnitConverter.length_to_si(val, unit)
                print(f"Результат в СИ: {res:.6f} м")
        except Exception as e:
            print(f"Ошибка: {e}")

    elif choice == '2':
        print("\n--- Расчет плотности rho(T, p) ---")
        rho20 = float(input("Плотность при 20°C rho20 [кг/м3]: "))
        temp = float(input("Температура T [°C]: "))
        press_mpa = float(input("Давление p [МПа] (например 0.1013 или 5.0): "))
        rho = FluidProperties.calc_density(rho20, temp, press_mpa * 1e6)
        print(f"\nРассчитанная плотность rho(T, p) = {rho:.3f} кг/м3")

    elif choice == '3':
        print("\n--- Комплексный расчет участка трубы ---")
        q_m3_h = float(input("Расход перекачки [м3/ч]: "))
        length_km = float(input("Длина участка [км]: "))
        diam_mm = float(input("Внутренний диаметр [мм]: "))
        rough_mm = float(input("Шероховатость k_e [мм] (типовая 0.1 мм): "))
        visc_cst = float(input("Кинематическая вязкость [сСт]: "))
        density = float(input("Плотность [кг/м3] (типовая 850 кг/м3): "))

        q_si = UnitConverter.volume_flow_to_si(q_m3_h, "м3/ч")
        l_si = UnitConverter.length_to_si(length_km, "км")
        d_si = UnitConverter.length_to_si(diam_mm, "мм")
        k_si = UnitConverter.length_to_si(rough_mm, "мм")
        nu_si = UnitConverter.viscosity_kinematic_to_si(visc_cst, "сСт")

        res = PipelineHydraulics.calc_pipe_losses(q_si, l_si, d_si, k_si, nu_si, density)

        print("\n" + "-" * 50)
        print("РЕЗУЛЬТАТЫ ГИДРАВЛИЧЕСКОГО РАСЧЕТА:")
        print(f"  Расход в СИ (Q):          {q_si:.6f} м3/с")
        print(f"  Скорость потока (v):      {res['velocity']:.4f} м/с")
        print(f"  Число Рейнольдса (Re):    {res['reynolds']:.1f}")
        print(f"  Режим течения:            {res['regime']}")
        print(f"  Коэффициент трения (lam): {res['friction_factor']:.5f}")
        print(f"  Потери напора (h_тр):     {res['head_loss_m']:.2f} м")
        print(f"  Гидравлический уклон (i): {res['hydraulic_gradient']:.6f} (м/м)")
        print(f"  Потери давления (dp):     {res['pressure_drop_mpa']:.4f} МПа ({res['pressure_drop_pa']:.1f} Па)")
        print(f"  Модуль сопротивления (s): {res['resistance_modulus_s']:.4e} с2/м5")
        print("-" * 50)

    elif choice == '4':
        print("\n--- Расчет прямого гидроудара Жуковского ---")
        density = float(input("Плотность нефти [кг/м3]: "))
        diam_mm = float(input("Внутренний диаметр [мм]: "))
        thick_mm = float(input("Толщина стенки трубы [мм]: "))
        length_km = float(input("Длина трубы [км]: "))
        delta_v = float(input("Сброс скорости delta_v [м/с]: "))

        d_si = diam_mm * 1e-3
        e_si = thick_mm * 1e-3
        l_si = length_km * 1000.0

        res = PipelineHydraulics.calc_water_hammer(density, d_si, e_si, l_si, delta_v)

        print("\n" + "-" * 50)
        print("ПАРАМЕТРЫ ГИДРОУДАРА:")
        print(f"  Скорость звука в трубе (c): {res['wave_speed_c']:.1f} м/с")
        print(f"  Фаза удара tau (2L/c):      {res['phase_tau_s']:.3f} с")
        print(f"  Скачок давления delta_p:    {res['delta_p_joukowsky_mpa']:.3f} МПа ({res['delta_p_joukowsky_pa']:.1f} Па)")
        print(f"  Скачок напора delta_H:      {res['delta_h_joukowsky_m']:.2f} м")
        print("-" * 50)


def main():
    if len(sys.argv) == 1:
        interactive_mode()
        return

    parser = argparse.ArgumentParser(description="Инженерный калькулятор гидравлики (Губкинский университет)")
    parser.add_argument("--q", type=float, help="Объемный расход [м3/с]")
    parser.add_argument("--d", type=float, help="Внутренний диаметр [м]")
    parser.add_argument("--l", type=float, help="Длина трубы [м]")
    parser.add_argument("--ke", type=float, default=0.0001, help="Шероховатость [м] (по умолч. 0.0001 м)")
    parser.add_argument("--nu", type=float, default=15e-6, help="Кинематическая вязкость [м2/с] (по умолч. 15 сСт)")
    parser.add_argument("--rho", type=float, default=850.0, help="Плотность [кг/м3] (по умолч. 850 кг/м3)")

    args = parser.parse_args()
    if args.q is not None and args.d is not None and args.l is not None:
        res = PipelineHydraulics.calc_pipe_losses(args.q, args.l, args.d, args.ke, args.nu, args.rho)
        print(f"v={res['velocity']:.4f} m/s, Re={res['reynolds']:.1f}, Regime={res['regime']}, lambda={res['friction_factor']:.5f}, dp={res['pressure_drop_mpa']:.4f} MPa, h_loss={res['head_loss_m']:.2f} m")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
